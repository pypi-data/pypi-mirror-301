import abc
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Generic, Optional, Sequence, TypeVar

import jax.random
import numpy as np
from jax.random import PRNGKey

from levanter.utils import thread_utils


logger = logging.getLogger(__name__)


T_co = TypeVar("T_co", covariant=True)
T = TypeVar("T")
U = TypeVar("U")


_executor = ThreadPoolExecutor(max_workers=10)


class DatasetBase(abc.ABC, Generic[T_co]):
    """
    Base class for sync and async datasets. This class is not meant to be used directly.
    """

    @abc.abstractmethod
    def as_async_dataset(self) -> "AsyncDataset[T_co]":
        raise NotImplementedError("...")

    @abc.abstractmethod
    def as_sync_dataset(self) -> "SyncDataset[T_co]":
        raise NotImplementedError("...")


class AsyncDataset(DatasetBase[T_co]):
    """
    An asynchronous dataset that can be used with async/await syntax. In Levanter, we use AsyncDataset for two purposes:
    * To represent datasets that are inherently asynchronous (e.g. reading from disk, network, etc.).
    * To represent datasets that are still being constructed.

    The core methods in this class are:
    * `async_len`: Returns the final length of the dataset.
    * `get_batch`: Returns a batch of items from the dataset.
    * `current_len`: Returns the current length of the dataset. This may be None if no current length is known.
    """

    @abc.abstractmethod
    async def async_len(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    async def final_length_is_known(self) -> bool:
        """Returns whether the final length of the dataset is known.
        If this returns False, the current_len of the dataset may change in the future."""
        raise NotImplementedError

    @abc.abstractmethod
    def is_finite(self) -> bool:
        """
        Returns whether the dataset will have a known length in the future (e.g. if it's being constructed).
        If this returns False, the length of the dataset is infinite or unknowable.
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def current_len(self) -> Optional[int]:
        """
        Returns the current length of the dataset that won't require (expensive) waiting.

        If the current length is not known, returns None. This might block temporarily for a short time to get the
        current length.
        """
        raise NotImplementedError

    async def getitem_async(self, index: int) -> T_co:
        """
        Returns the item at the given index. Typically implemented as a wrapper around `get_batch`.

        In general, it is better to call (and override) `get_batch` instead of this method.
        """
        return (await self.get_batch([index]))[0]

    @abc.abstractmethod
    async def get_batch(self, indices: Sequence[int]) -> Sequence[T_co]:
        raise NotImplementedError

    async def wait_until_len_at_least(self, length: int) -> int:
        """
        Returns the length of the dataset once it is at least `length` or if the dataset has a known (finished) length.

        The default implementation is a naive busy-wait loop. You should override this method for more efficient
        implementations.
        """
        return await naive_busy_wait_until_len_at_least(self, length)

    def as_sync_dataset(self):
        return SyncifiedDataset(self)

    def as_async_dataset(self) -> "AsyncDataset[T_co]":
        return self

    def map(self, fn: Callable[[T_co], U], *extra_args, **extra_kwargs) -> "MappedAsyncDataset[T_co, U]":
        return MappedAsyncDataset(self, fn, *extra_args, **extra_kwargs)

    def shuffle(self, key: PRNGKey):
        import levanter.data.permutation as permutation

        return permutation.PermutationDataset(self, key)

    def era_shuffle(self, era_length: int, key: PRNGKey):
        import levanter.data.permutation as permutation

        return permutation.EraShufflingDataset(self, era_length, key=key)


async def naive_busy_wait_until_len_at_least(dataset: AsyncDataset[T_co], length: int) -> int:
    """
    Runs a busy-wait loop until the dataset has at least `length` items or the final length is known.

    Returns the current length of the dataset when either the dataset has at least `length` items or the final length is
    known.

    You should probably implement this in a more efficient way. This is just a naive implementation.
    """
    while not await dataset.final_length_is_known():
        current_len = await dataset.current_len()
        if current_len is None:
            raise ValueError("Dataset has unknown length")
        if current_len <= length:
            await asyncio.sleep(0.1)
        else:
            return current_len

    return await dataset.async_len()


class SyncDataset(DatasetBase[T_co]):
    """
    A synchronous dataset that can be used with regular Python syntax. In Levanter, we mainly do not use this class.
    You can use this class if it's easier, then convert it to an AsyncDataset using `as_async_dataset`. This
    is not as efficient as using an AsyncDataset directly, but it can be useful for testing or for simpler code.
    """

    @abc.abstractmethod
    def __len__(self) -> int:
        """
        Returns the final length of the data store.
        May raise if the length is not known.
        """

    @abc.abstractmethod
    def has_len(self) -> bool:
        """
        Whether the data store currently has a known length. If this returns False, then the length of the data store
        may change in the future.
        """
        pass

    @abc.abstractmethod
    def current_len(self) -> Optional[int]:
        """
        Returns the current length of the data store. If the length is infinite or not known, returns None.
        """
        pass

    def __getitem__(self, index: int) -> T_co:
        return self.get_batch([index])[0]

    @abc.abstractmethod
    def get_batch(self, indices: Sequence[int] | np.ndarray) -> Sequence[T_co]:
        pass

    def as_async_dataset(self) -> "AsyncDataset[T_co]":
        return AsyncifiedDataset(self)

    def as_sync_dataset(self) -> "SyncDataset[T_co]":
        return self


class SyncifiedDataset(SyncDataset[T_co]):
    def __init__(self, dataset: AsyncDataset[T_co]):
        self.dataset = dataset

    def _run_coroutine(self, coro):
        return thread_utils.blocking_wait(coro)

    def __len__(self) -> int:
        return self._run_coroutine(self.dataset.async_len())

    def has_len(self) -> bool:
        return self.dataset.is_finite()

    def current_len(self) -> Optional[int]:
        return self._run_coroutine(self.dataset.current_len())

    def get_batch(self, indices: Sequence[int] | np.ndarray) -> Sequence[T_co]:
        return self._run_coroutine(self.dataset.get_batch(indices))

    def __getitem__(self, index: int) -> T_co:
        return self._run_coroutine(self.dataset.getitem_async(index))


class AsyncifiedDataset(AsyncDataset[T_co]):
    def __init__(self, dataset: SyncDataset[T_co]):
        self.dataset = dataset

    async def async_len(self) -> int:
        return len(self.dataset)

    async def final_length_is_known(self) -> bool:
        return self.dataset.has_len()

    def is_finite(self) -> bool:
        return self.dataset.has_len()

    async def current_len(self) -> Optional[int]:
        return self.dataset.current_len()

    async def get_batch(self, indices: Sequence[int]) -> Sequence[T_co]:
        return self.dataset.get_batch(indices)

    async def getitem_async(self, index: int) -> T_co:
        return self.dataset[index]

    def __repr__(self):
        return f"WrappedAsyncDataset({repr(self.dataset)})"

    def __str__(self):
        return f"WrappedAsyncDataset({str(self.dataset)})"


class ListAsyncDataset(AsyncDataset[T]):
    """
    A simple dataset that wraps a list. Mostly for testing.
    """

    def __init__(self, data: list[T], is_complete: bool = False):
        self.data = data
        self.is_complete = is_complete
        if not is_complete:
            self.complete_promise: Optional[asyncio.Future[None]] = asyncio.Future()
            self.length_updated: Optional[asyncio.Condition] = asyncio.Condition()
        else:
            self.complete_promise = None
            self.length_updated = None

    async def async_len(self) -> int:
        # this is the final length
        if not self.is_complete:
            assert self.complete_promise is not None
            await self.complete_promise
        return len(self.data)

    async def final_length_is_known(self) -> bool:
        return self.is_complete

    def is_finite(self) -> bool:
        return True

    async def current_len(self) -> Optional[int]:
        return len(self.data)

    async def get_batch(self, indices: Sequence[int]) -> Sequence[T]:
        await self.wait_until_len_at_least(max(indices) + 1)
        return [self.data[i] for i in indices]

    def append(self, item: T):
        if self.is_complete:
            raise ValueError("Cannot append to a finalized dataset")
        self.data.append(item)
        asyncio.create_task(self.notify_length_update())

    def finalize(self):
        self.is_complete = True
        if self.complete_promise is not None:
            self.complete_promise.set_result(None)
            if not asyncio.get_event_loop().is_running():
                _executor.submit(lambda: asyncio.run(self.notify_length_update()))
            else:
                asyncio.create_task(self.notify_length_update())

    async def notify_length_update(self):
        async with self.length_updated:
            self.length_updated.notify_all()

    async def wait_until_len_at_least(self, length: int) -> int:
        if self.is_complete:
            return len(self.data)

        assert self.length_updated is not None

        async with self.length_updated:
            while len(self.data) < length and not self.is_complete:
                await self.length_updated.wait()

        return len(self.data)


class MappedAsyncDataset(AsyncDataset[U], Generic[T, U]):
    """
    A dataset that applies a function to each item in the dataset.
    You can pass extra arguments to the function using `*extra_args` and `**extra_kwargs`.
    If a kwarg called `key` is passed, it will be treated as a PRNGKey and folded in with the index of the item
    for each call to the function.
    """

    def __init__(
        self,
        dataset: AsyncDataset[T],
        fn: Callable[[T], U] | Callable[[T, Optional[PRNGKey]], U],
        *extra_args,
        **extra_kwargs,
    ):
        self.dataset = dataset
        self.fn = fn
        self._extra_args = extra_args
        self._extra_kwargs = extra_kwargs

    async def async_len(self) -> int:
        return await self.dataset.async_len()

    async def final_length_is_known(self) -> bool:
        return await self.dataset.final_length_is_known()

    def is_finite(self) -> bool:
        return self.dataset.is_finite()

    async def current_len(self) -> Optional[int]:
        return await self.dataset.current_len()

    def _maybe_fold_in_key(self, key, index):
        if key is not None:
            key = jax.random.fold_in(key, index)
        return key

    async def get_batch(self, indices: Sequence[int]) -> Sequence[U]:
        items = await self.dataset.get_batch(indices)
        return [self._call_fn(i, item) for i, item in zip(indices, items)]

    async def getitem_async(self, index: int) -> U:
        return self._call_fn(index, await self.dataset.getitem_async(index))

    async def wait_until_len_at_least(self, length: int) -> int:
        return await self.dataset.wait_until_len_at_least(length)

    def _call_fn(self, index, item):
        if "key" in self._extra_kwargs:
            key = self._maybe_fold_in_key(self._extra_kwargs["key"], index)
            kwargs = {**self._extra_kwargs, "key": key}
        else:
            kwargs = self._extra_kwargs
        return self.fn(item, *self._extra_args, **kwargs)

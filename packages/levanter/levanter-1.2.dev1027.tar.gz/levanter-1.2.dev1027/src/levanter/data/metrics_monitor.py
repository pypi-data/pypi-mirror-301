import dataclasses
import logging as pylogging
import threading
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional, Protocol, Union

import jax
from dataclasses_json import dataclass_json
from rich.progress import (
    BarColumn,
    Progress,
    TaskID,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)

import levanter.tracker


# TODO: should we just make the ledger have all this?
@dataclass_json
@dataclass
class InProgressCacheMetrics:
    rows_finished: int = 0
    shards_finished: int = 0
    field_counts: Dict[str, int] = dataclasses.field(default_factory=dict)
    is_finished: bool = False


class MetricsMonitor(Protocol):
    def __call__(self, metrics: InProgressCacheMetrics):
        ...


class RichMetricsMonitor(MetricsMonitor):

    progress: Optional[Progress]  # type: ignore
    task: Optional[TaskID]

    def __init__(self, num_shards, **kwargs):
        """kwargs are passed to rich.progress.Progress"""
        self.kwargs = kwargs
        self.progress: Optional[Progress] = None
        self.task = None
        self.num_shards = num_shards

    def __call__(self, metrics: InProgressCacheMetrics):
        if self.progress is None:
            self._init_progress(metrics)

        self.progress.update(self.task, completed=metrics.shards_finished, **dataclasses.asdict(metrics))  # type: ignore

        self.progress.refresh()  # type: ignore

        if metrics.is_finished:
            self.progress.stop()  # type: ignore

    def _init_progress(self, metrics):
        columns = [
            BarColumn(),
            TaskProgressColumn(),
            TextColumn("| {task.fields[rows_finished]} docs", justify="center"),
        ]

        for field in metrics.field_counts:
            columns.append(TextColumn(f"| {{task.fields[field_counts][{field}]}} {field}", justify="center"))

        columns.append(TimeElapsedColumn())
        columns.append(TimeRemainingColumn())

        self.progress = Progress(
            *columns,
            **self.kwargs,
        )

        self.task = self.progress.add_task(
            "Shards", total=self.num_shards, completed=metrics.shards_finished, **dataclasses.asdict(metrics)
        )
        self.progress.start()


class LoggingMetricsMonitor(MetricsMonitor):
    last_metrics: Optional[InProgressCacheMetrics]
    last_time: Optional[float]

    def __init__(self, prefix: str = "preproc", commit=False):
        """
        :param prefix:
        :param commit: Forwarded to wandb.log. Use False (default) if it's part of a simultaneous training run,
        and True if you're running standalone.
        """
        self.prefix = prefix
        self.commit = commit
        self.last_metrics = None
        self.last_time = None

    def __call__(self, metrics: InProgressCacheMetrics):
        to_log: Dict[str, Any] = {}

        to_log[f"{self.prefix}/shards"] = metrics.shards_finished
        to_log[f"{self.prefix}/rows"] = metrics.rows_finished

        for field, count in metrics.field_counts.items():
            to_log[f"{self.prefix}/{field}"] = count

        if metrics.is_finished:
            to_log[f"{self.prefix}/finished"] = 1

        # estimate the rate of progress
        # if self.last_metrics is not None:
        #     assert self.last_time is not None
        #     elapsed = time.time() - self.last_time
        #     to_log[f"{self.prefix}/shards_per_s"] = (metrics.shards_finished - self.last_metrics.shards_finished) / elapsed
        #     to_log[f"{self.prefix}/rows_per_s"] = (metrics.rows_finished - self.last_metrics.rows_finished) / elapsed
        #
        #     for field, count in metrics.field_counts.items():
        #         to_log[f"{self.prefix}/{field}_per_s"] = (count - self.last_metrics.field_counts[field]) / elapsed

        self.last_metrics = metrics
        self.last_time = time.time()

        levanter.tracker.log_metrics(to_log, step=None, commit=self.commit)


class LoggerMetricsMonitor(MetricsMonitor):
    # TODO: I'd like to get the trainer pbar migrated to rich and just use rich everywhere, but until then,
    # we have separate logging
    def __init__(
        self,
        logger: Optional[Union[pylogging.Logger, str]] = None,
        level=pylogging.INFO,
        log_interval: float | int = 30.0,
    ):
        if isinstance(logger, str):
            logger = pylogging.getLogger(logger)
        self.logger = logger or pylogging.getLogger(__name__)
        self.level = level
        self.log_interval = log_interval
        self._last_log_time = time.time()

    def __call__(self, metrics: InProgressCacheMetrics):
        if jax.process_index() == 0:
            if time.time() - self._last_log_time > self.log_interval:
                self._last_log_time = time.time()

                self.logger.log(
                    self.level,
                    f" done: Shards: {metrics.shards_finished} | Docs: {metrics.rows_finished}",
                )

        if metrics.is_finished:
            self.logger.info("Cache creation finished")


class WaitTimeReportingThread(threading.Thread):
    def __init__(self, report, interval=60):
        super().__init__()
        self.report = report
        self.interval = interval
        self.shutdown_event = threading.Event()

    def run(self):
        total_waited = 0
        while True:
            if self.shutdown_event.wait(self.interval):
                break
            if total_waited > 0:
                self.report(total_waited)
            total_waited += self.interval

    def shutdown(self):
        self.shutdown_event.set()

from collections.abc import Callable, Coroutine
from enum import IntFlag
from typing import Any

JobCallback = Callable[..., Coroutine[Any, Any, Any]]


class EventType(IntFlag):
    EVENT_SCHEDULER_STARTED = 1 << 0
    EVENT_SCHEDULER_SHUTDOWN = 1 << 1
    EVENT_SCHEDULER_PAUSED = 1 << 2
    EVENT_SCHEDULER_RESUMED = 1 << 3
    EVENT_EXECUTOR_ADDED = 1 << 4
    EVENT_EXECUTOR_REMOVED = 1 << 5
    EVENT_JOB_STORE_ADDED = 1 << 6
    EVENT_JOB_STORE_REMOVED = 1 << 7
    EVENT_ALL_JOBS_REMOVED = 1 << 8
    EVENT_JOB_ADDED = 1 << 9
    EVENT_JOB_REMOVED = 1 << 10
    EVENT_JOB_MODIFIED = 1 << 11
    EVENT_JOB_EXECUTED = 1 << 12
    EVENT_JOB_ERROR = 1 << 13
    EVENT_JOB_MISSED = 1 << 14
    EVENT_JOB_SUBMITTED = 1 << 15
    EVENT_JOB_MAX_INSTANCES = 1 << 16
    EVENT_ALL = (
        EVENT_SCHEDULER_STARTED
        | EVENT_SCHEDULER_SHUTDOWN
        | EVENT_SCHEDULER_PAUSED
        | EVENT_SCHEDULER_RESUMED
        | EVENT_EXECUTOR_ADDED
        | EVENT_EXECUTOR_REMOVED
        | EVENT_JOB_STORE_ADDED
        | EVENT_JOB_STORE_REMOVED
        | EVENT_ALL_JOBS_REMOVED
        | EVENT_JOB_ADDED
        | EVENT_JOB_REMOVED
        | EVENT_JOB_MODIFIED
        | EVENT_JOB_EXECUTED
        | EVENT_JOB_ERROR
        | EVENT_JOB_MISSED
        | EVENT_JOB_SUBMITTED
        | EVENT_JOB_MAX_INSTANCES
    )

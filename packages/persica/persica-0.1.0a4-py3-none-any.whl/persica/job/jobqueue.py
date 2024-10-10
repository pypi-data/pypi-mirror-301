from collections.abc import Callable
from datetime import datetime, time, timedelta
from typing import TYPE_CHECKING

import pytz
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger

from persica.job.types import JobCallback

if TYPE_CHECKING:
    from pytz.tzinfo import BaseTzInfo

    from persica.job.types import EventType


class JobQueue:
    def __init__(self, timezone: "BaseTzInfo" = pytz.utc):
        self._executor = AsyncIOExecutor()
        scheduler_configuration = {
            "timezone": timezone,
            "executors": {"default": self._executor},
        }
        self.scheduler: AsyncIOScheduler = AsyncIOScheduler(**scheduler_configuration)

    def add_listener(self, callback: Callable, mask: "EventType"):
        self.scheduler.add_listener(callback, mask.value())

    def run_once(
        self,
        callback: JobCallback,
        when: datetime,
        args: list | None = None,
        kwargs: dict | None = None,
        job_id: str | None = None,
    ):
        trigger = DateTrigger(run_date=when)
        self.scheduler.add_job(
            callback,
            trigger,
            args=args,
            kwargs=kwargs,
            id=job_id,
            replace_existing=True,
        )

    def run_repeating(
        self,
        callback: JobCallback,
        interval: float | timedelta,
        first: datetime | None = None,
        last: datetime | None = None,
        args: list | None = None,
        kwargs: dict | None = None,
        job_name: str | None = None,
    ):
        """以固定的时间间隔重复运行任务。"""
        if isinstance(interval, timedelta):
            interval = interval.total_seconds()

        name = job_name or callback.__name__
        trigger = IntervalTrigger(
            seconds=interval,
            start_date=first,
            end_date=last,
            timezone=self.scheduler.timezone,
        )
        self.scheduler.add_job(callback, trigger, args=args, kwargs=kwargs, id=name, replace_existing=True)

    def run_daily(
        self,
        callback: JobCallback,
        time_of_day: time,
        days: list | None = None,
        args: list | None = None,
        kwargs: dict | None = None,
        job_id: str | None = None,
    ):
        """每天在指定的时间运行任务。"""
        days = days or ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
        trigger = CronTrigger(
            day_of_week=",".join(days),
            hour=time_of_day.hour,
            minute=time_of_day.minute,
            second=time_of_day.second,
            timezone=self.scheduler.timezone,
        )
        self.scheduler.add_job(
            callback,
            trigger,
            args=args,
            kwargs=kwargs,
            id=job_id,
            replace_existing=True,
        )

    def run_monthly(
        self,
        callback: JobCallback,
        day: int,
        time_of_day: time,
        args: list | None = None,
        kwargs: dict | None = None,
        job_id: str | None = None,
    ):
        """每月在指定的日期和时间运行任务。"""
        trigger = CronTrigger(
            day=day,
            hour=time_of_day.hour,
            minute=time_of_day.minute,
            second=time_of_day.second,
            timezone=self.scheduler.timezone,
        )
        self.scheduler.add_job(
            callback,
            trigger,
            args=args,
            kwargs=kwargs,
            id=job_id,
            replace_existing=True,
        )

    def get_jobs_by_name(self, name: str) -> tuple[Job, ...]:
        return tuple(job for job in self.scheduler.get_jobs() if job.name == name)

from datetime import date
from functools import partial, update_wrapper
from time import sleep

from .config import Config
from .job import Job
from .utils import get_active_period_window, get_period_window

config = Config()
jobs_list = []


def set_configs(start_day=0, start_date=date.today()):
    config._set_configs(start_day, start_date)
    config.get_configs()


def first(active_interval=1):
    active_period = ActivePeriod(active_interval, "FIRST")
    return active_period


def last(active_interval=1):
    active_period = ActivePeriod(active_interval, "LAST")
    return active_period


class ActivePeriod(object):
    def __init__(self, active_interval, active_period):
        self.active_interval = active_interval
        self.active_duration = None
        self.active_period = active_period

    @property
    def days(self):
        self.active_duration = "DAYS"
        return self

    @property
    def weeks(self):
        self.active_duration = "WEEKS"
        return self

    @property
    def months(self):
        self.active_duration = "MONTHS"
        return self

    def of(self, recurring_interval=1):
        recurring_period = RecurringPeriod(
            self.active_period, self.active_interval, self.active_duration, recurring_interval
        )
        return recurring_period


class RecurringPeriod(object):
    def __init__(self, active_period, active_interval, active_duration, recurring_interval):
        self.active_period = active_period
        self.active_interval = active_interval
        self.active_duration = active_duration
        self.recurring_interval = recurring_interval
        self.recurring_duration = None

    @property
    def days(self):
        self.recurring_duration = "DAYS"
        return self

    @property
    def weeks(self):
        self.recurring_duration = "WEEKS"
        return self

    @property
    def months(self):
        self.recurring_duration = "MONTHS"
        return self

    def every(self, interval=1):
        today_date = date.today()
        start_day, start_date = config.get_configs()
        window_start_date, window_end_date = get_period_window(
            start_date, self.recurring_duration, self.recurring_interval, today_date, start_day
        )
        active_start_date, active_end_date = get_active_period_window(
            self.active_duration,
            self.active_period,
            self.active_interval,
            start_day,
            window_start_date,
            window_end_date,
        )
        print(active_start_date, active_end_date)
        activetime = ActiveTime(active_start_date, active_end_date, interval)
        return activetime


class ActiveTime(object):
    def __init__(self, active_start_date, active_end_date, interval):
        self.active_start_date = active_start_date
        self.active_end_date = active_end_date
        self.interval = interval
        self.active_time = None

    @property
    def seconds(self):
        self.active_time = "SECONDS"
        return self

    @property
    def minutes(self):
        self.active_time = "MINUTES"
        return self

    @property
    def hours(self):
        self.active_time = "HOURS"
        return self

    @property
    def days(self):
        self.active_time = "DAYS"
        return self

    def do(self, job_func, *args, **kwargs):
        if self.active_time is "MINUTES":
            self.interval = self.interval * 60
        if self.active_time is "HOURS":
            self.interval = self.interval * 3600
        while True:
            if self.active_start_date <= date.today() <= self.active_end_date:
                job_func()
                sleep(self.interval)

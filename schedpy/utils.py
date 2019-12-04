from calendar import monthrange
from datetime import date, timedelta


class ScheduleSelectionError(Exception):
    """Schedule selection exception"""

    pass


def add_months(given_date, months, days):
    month = given_date.month - 1 + months
    year = given_date.year + (month // 12)
    month = month % 12 + 1
    day = min(given_date.day, monthrange(year, month)[1])
    return date(year, month, day) - timedelta(1)


def get_week_start_date(given_date, start_day):
    days_diff = 7 + given_date.weekday() - start_day
    if given_date.weekday() - start_day >= 0:
        days_diff = given_date.weekday() - start_day
    return given_date - timedelta(days_diff)


def end_date_after_n_weeks(start_date, active_value, start_day):
    return get_week_start_date(start_date, start_day) + timedelta(7 * active_value - 1)


def start_date_before_n_weeks(end_date, active_value, start_day):
    return get_week_start_date(end_date, start_day) + timedelta(-7 * (active_value - 1))


def get_period_window(start_date, period, period_value, today_date, start_day):
    if period == "MONTHS":
        end_date = add_months(start_date, period_value, 1)
        while today_date > end_date:
            start_date = end_date + timedelta(1)
            end_date = add_months(start_date, period_value, 1)
    elif period == "WEEKS":
        end_date = end_date_after_n_weeks(start_date, period_value, start_day)
        while today_date > end_date:
            start_date = end_date + timedelta(1)
            end_date = end_date_after_n_weeks(start_date, period_value, start_day)
    elif period == "DAYS":
        end_date = start_date + timedelta(period_value)
        while today_date > end_date:
            start_date = end_date + timedelta(period_value)
            end_date = start_date + timedelta(period_value)
    return start_date, end_date


def get_active_period_window(active_period, active_type, active_value, start_day, start_date, end_date):
    active_start_date = start_date
    active_end_date = end_date
    if active_period == "MONTHS":
        if active_type == "FIRST":
            active_end_date = add_months(start_date, active_value, 1)
        else:
            active_start_date = add_months(end_date + timedelta(1), -active_value, 0)
    elif active_period == "WEEKS":
        if active_type == "FIRST":
            active_end_date = end_date_after_n_weeks(start_date, active_value, start_day)
        else:
            active_start_date = start_date_before_n_weeks(end_date, active_value, start_day)
    elif active_period == "DAYS":
        if active_type == "FIRST":
            active_end_date = start_date + timedelta(active_value - 1)
        else:
            active_start_date = end_date - timedelta(active_value - 1)
    if active_start_date < start_date or active_end_date > end_date:
        raise ScheduleSelectionError("Active date range overflow")
    return active_start_date, active_end_date

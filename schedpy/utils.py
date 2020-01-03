from calendar import monthrange
from datetime import date, timedelta


class ScheduleSelectionError(Exception):
    """Schedule selection exception"""

    pass


def add_months(given_date, months, days):
    """Function to add months (positive or non-positive) to the date given.

    Args:
        given_date: The given date.
        months: Number of months to be added.
        days: Number of days to go back from the final date.

    Returns:
        Final computed date after n months.
    """
    month = given_date.month - 1 + months
    year = given_date.year + (month // 12)
    month = month % 12 + 1
    day = min(given_date.day, monthrange(year, month)[1])
    return date(year, month, day) - timedelta(days)


def get_week_start_date(given_date, start_day):
    """ Function to get the start date of the week depending on the start day.

    Args:
        given_date: The given date.
        start_day: Start day of the week.

    Returns:
        Week's start date.
    """
    days_diff = 7 + given_date.weekday() - start_day
    if given_date.weekday() - start_day >= 0:
        days_diff = given_date.weekday() - start_day
    return given_date - timedelta(days_diff)


def end_date_after_n_weeks(start_date, n, start_day):
    """Function to get the end date after n weeks.

    Args:
        start_date: given start date.
        n: Number of weeks.
        start_day: Start day of the week.

    Returns:
        End date of the week after n weeks from the start date.
    """
    return get_week_start_date(start_date, start_day) + timedelta(7 * n - 1)


def start_date_before_n_weeks(end_date, n, start_day):
    """Function to get the start date before n weeks.

    Args:
        end_date: given end date.
        n: Number of weeks.
        start_day: Start day of the week.

    Returns:
        Start date of the week before n weeks from the end date.
    """
    return get_week_start_date(end_date, start_day) + timedelta(-7 * (n - 1))


def get_period_window(start_date, period, period_value, today_date, start_day):
    """Function to get the period window containing the active window and today's date.

    Args:
        start_date: given start date.
        period: May be Months, Weeks or Days.
        period_value: Number of period (Months, Weeks or Days)
        today_date: Today's date.
        start_day: Start day of the week.

    Returns:
        Tuple containing start and end date.
    """
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
    """Function to get active period window from period window.

    Args:
        active_period: May be Months, Weeks or Days.
        active_type: May be First or Last.
        active_value: Number of active_period (Months, Weeks or Days).
        start_day: Start day of the week.
        start_date: Start date of the period window.
        end_date: End date of the period window.

    Returns:
        Tuple containing active start and end date.
    """
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

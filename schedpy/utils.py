from calendar import monthrange
from datetime import date, timedelta


class ScheduleSelectionError(Exception):
    """Schedule selection exception"""

    pass


def add_months(given_date, months, days):
    """Function to add months (positive or non-positive) to the date given.

    Parameters
    ==========

    given_date: The given date.
    months: Number of months to be added.
    days: Number of days to go back from the final date.

    Returns
    =======

    Final computed date after n months.

    Examples
    ========

    >>> from schedpy.utils import add_months
    >>> from datetime import date
    >>> d = date(2019, 12, 1)
    >>> add_months(d, 2, 1)
    datetime.date(2020, 1, 31)
    >>> add_months(d, 3, 1)
    datetime.date(2020, 2, 29)
    """
    month = given_date.month - 1 + months
    year = given_date.year + (month // 12)
    month = month % 12 + 1
    day = min(given_date.day, monthrange(year, month)[1])
    return date(year, month, day) - timedelta(days)


def get_week_start_date(given_date, start_day):
    """ Function to get the start date of the week depending on the start day.

    Parameters
    ==========

    given_date: The given date.
    start_day: Start day of the week.

    Returns
    =======

    Week's start date.

    Examples
    ========

    >>> from schedpy.utils import get_week_start_date
    >>> d = date(2019, 12, 1)
    >>> get_week_start_date(d, 1)
    datetime.date(2019, 11, 26)
    >>> get_week_start_date(d, 3)
    datetime.date(2019, 11, 28)
    """
    days_diff = 7 + given_date.weekday() - start_day
    if given_date.weekday() - start_day >= 0:
        days_diff = given_date.weekday() - start_day
    return given_date - timedelta(days_diff)


def end_date_after_n_weeks(start_date, n, start_day):
    """Function to get the end date after n weeks.

    Parameters
    ==========

    start_date: given start date.
    n: Number of weeks.
    start_day: Start day of the week.

    Returns
    =======

    End date of the week after n weeks from the start date.

    Examples
    ========
    >>> from schedpy.utils import end_date_after_n_weeks
    >>> from datetime import date, timedelta
    >>> end_date_after_n_weeks(date(2019, 12, 13), 5, 0)
    datetime.date(2020, 1, 12)
    >>> end_date_after_n_weeks(date(2019, 12, 1), 3, 5)
    datetime.date(2019, 12, 20)

    """
    return get_week_start_date(start_date, start_day) + timedelta(7 * n - 1)


def start_date_before_n_weeks(end_date, n, start_day):
    """Function to get the start date before n weeks.

    Parameters
    ==========

    end_date: given end date.
    n: Number of weeks.
    start_day: Start day of the week.

    Returns
    =======

    Start date of the week before n weeks from the end date.

    Examples
    ========
    >>> from schedpy.utils import start_date_before_n_weeks
    >>> from datetime import date, timedelta
    >>> start_date_before_n_weeks(date(2019, 12, 13), 3, 3)
    datetime.date(2019, 11, 28)
    >>> start_date_before_n_weeks(date(2019, 1, 13), 3, 3)
    datetime.date(2018, 12, 27)
    """
    return get_week_start_date(end_date, start_day) + timedelta(-7 * (n - 1))


def get_period_window(start_date, period, period_value, today_date, start_day):
    """Function to get the period window containing the active window and today's date.

    Parameters
    ==========

    start_date: given start date.
    period: May be Months, Weeks or Days.
    period_value: Number of period (Months, Weeks or Days)
    today_date: The date you want to start with.
    start_day: Start day of the week.

    Returns
    =======

    Tuple containing start and end date.

    Examples
    ========
    >>> from schedpy.utils import get_period_window, add_months
    >>> from datetime import date, timedelta
    >>> start_date = date(2019, 12, 3)
    >>> today_date = date(2020,10, 14)
    >>> get_period_window(start_date, "MONTHS", 3, today_date, 2)
    (datetime.date(2020, 9, 3), datetime.date(2020, 12, 2))
    >>> get_period_window(start_date, "DAYS", 5, today_date, 4)
    (datetime.date(2020, 10, 10), datetime.date(2020, 10, 15))
    >>> get_period_window(start_date, "WEEKS", 6, today_date, 0)
    (datetime.date(2020, 9, 21), datetime.date(2020, 11, 1))
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
            start_date = end_date + timedelta(1)
            end_date = start_date + timedelta(period_value)
    return start_date, end_date


def get_active_period_window(active_period, active_type, active_value, start_day, start_date, end_date):
    """Function to get active period window from period window.

    Parameters
    ==========

    active_period: May be Months, Weeks or Days.
    active_type: May be First or Last.
    active_value: Number of active_period (Months, Weeks or Days).
    start_day: Start day of the week.
    start_date: Start date of the period window.
    end_date: End date of the period window.

    Returns
    =======

    Tuple containing active start and end date.

    Examples
    ========
    >>> from schedpy.utils import get_active_period_window
    >>> from datetime import date, timedelta
    >>> get_active_period_window("MONTHS", "LAST", 2, 0, date(2019, 12, 1), date(2020, 2, 3))
    (datetime.date(2019, 12, 4), datetime.date(2020, 2, 3))
    >>> get_active_period_window("WEEKS", "LAST", 2, 0, date(2019, 12, 1), date(2020, 2, 3))
    (datetime.date(2020, 1, 27), datetime.date(2020, 2, 3))
    >>> get_active_period_window("WEEKS", "FIRST", 2, 0, date(2019, 12, 1), date(2020, 2, 3))
    (datetime.date(2019, 12, 1), datetime.date(2019, 12, 8))
    >>> get_active_period_window("MONTHS", "FIRST", 2, 0, date(2019, 12, 1), date(2020, 2, 3))
    (datetime.date(2019, 12, 1), datetime.date(2020, 1, 31))
    >>> get_active_period_window("DAYS", "FIRST", 21, 0, date(2019, 12, 1), date(2020, 2, 3))
    (datetime.date(2019, 12, 1), datetime.date(2019, 12, 21))
    >>> get_active_period_window("DAYS", "LAST", 21, 0, date(2019, 12, 1), date(2020, 2, 3))
    (datetime.date(2020, 1, 14), datetime.date(2020, 2, 3))

    """
    active_start_date = start_date
    active_end_date = end_date
    if active_period == "MONTHS":
        if active_type == "FIRST":
            active_end_date = add_months(start_date, active_value, 1)
        elif active_type == "LAST":
            active_start_date = add_months(end_date + timedelta(1), -active_value, 0)
    elif active_period == "WEEKS":
        if active_type == "FIRST":
            active_end_date = end_date_after_n_weeks(start_date, active_value, start_day)
        elif active_type == "LAST":
            active_start_date = start_date_before_n_weeks(end_date, active_value, start_day)
    elif active_period == "DAYS":
        if active_type == "FIRST":
            active_end_date = start_date + timedelta(active_value - 1)
        elif active_type == "LAST":
            active_start_date = end_date - timedelta(active_value - 1)
    if active_start_date < start_date or active_end_date > end_date:
        raise ScheduleSelectionError("Active date range overflow")
    return active_start_date, active_end_date

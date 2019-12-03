from datetime import date, timedelta
import calendar


def add_months(source_date, months, days):
    """Method to add months positive or non positive to the source_date.

    Args:
        source_date: The given date.
        months: Number of months to be added.

    Returns:
        Date after the given number of months.
    """

    month = source_date.month - 1 + months
    year = source_date.year + (month // 12)
    month = month % 12 + 1
    day = min(source_date.day, calendar.monthrange(year, month)[1])
    return date(year, month, day) - timedelta(days=1)


def get_week_start_date(source_date, start_day_index):
    """Method to get start date of the week the source_date is present as per the start day index

    Args:
        source_date: The given date.
        start_day_index: Index of the day week starts from (0-6 for Monday-Sunday repectively)

    Returns:
        Date of the first day of week the source_date lies in.
    """

    delta_days = (
        source_date.weekday() - start_day_index
        if source_date.weekday() - start_day_index >= 0
        else 7 + source_date.weekday() - start_day_index
    )
    return source_date - timedelta(days=delta_days)


def last_date_after_n_weeks(start_date, active_value, start_day_index):
    """Method to get the last date of the week after active_value weeks.

    Args:
        start_date: The given date to start from.
        active_value: Number of week.
        start_day_index: Index of the day week starts from (0-6 for Monday-Sunday repectively)

    Returns:
        Last date after active_value weeks.
    """

    days = 7 * active_value - 1
    return get_week_start_date(start_date, start_day_index) + timedelta(days=days)


def first_date_before_n_weeks(end_date, active_value, start_day_index):
    """Method to get the first date of the week before active_value weeks.

    Args:
        end_date: The given date to end at.
        active_value: Number of week.
        start_day_index: Index of the day week starts from (0-6 for Monday-Sunday repectively)

    Returns:
        First date before active_value weeks.
    """

    days = -7 * (active_value - 1)
    return get_week_start_date(end_date, start_day_index) + timedelta(days=days)


def get_latest_time_period_window(start_date, time_period, time_period_value, today_date, start_day_index):
    """Method to get the start and end date iterating with time_period_value such
    that today's date lies in the range.

    Args:
        start_date: The given date to start from.
        time_period: Type of time period months or weeks.
        time_period_value: Value of the given time period type.
        today_date: Today's date.
        start_day_index: Index of the day week starts from (0-6 for Monday-Sunday repectively)

    Returns:
        Start and end dates.
    """

    if time_period == "MONTHS":
        end_date = add_months(start_date, time_period_value, 1)
        while today_date > end_date:
            start_date = end_date + timedelta(days=1)
            end_date = add_months(start_date, time_period_value, 1)
    elif time_period == "WEEKS":
        end_date = last_date_after_n_weeks(start_date, time_period_value, start_day_index)
        while today_date > end_date:
            start_date = end_date + timedelta(days=1)
            end_date = last_date_after_n_weeks(start_date, time_period_value, start_day_index)
    return start_date, end_date


def get_active_period_window(active_period, active_type, active_value, start_day_index, start_date, end_date):
    """Method to get the active start and end date.

    Args:
        active_period: period of active months, weeks, days.
        active_type: type of active first or last.
        active_value: no. of active_period.
        start_day_index: Index of the day week starts from (0-6 for Monday-Sunday repectively)
        start_date: The given date to start from.
        end_date: The given date to end at.

    Returns:
        Start and end date of the active period window.
    """
    active_start_date = start_date
    active_end_date = end_date
    if active_period == "MONTHS":
        if active_type == "FIRST":
            active_end_date = add_months(start_date, active_value, 1)
        elif active_type == "LAST":
            active_start_date = add_months(end_date + timedelta(days=1), -active_value, 0)
    elif active_period == "WEEKS":
        if active_type == "FIRST":
            active_end_date = last_date_after_n_weeks(start_date, active_value, start_day_index)
        elif active_type == "LAST":
            active_start_date = first_date_before_n_weeks(end_date, active_value, start_day_index)
    elif active_period == "DAYS":
        if active_type == "FIRST":
            active_end_date = start_date + timedelta(days=active_value - 1)
        elif active_type == "LAST":
            active_start_date = end_date - timedelta(days=active_value - 1)
    return active_start_date, active_end_date

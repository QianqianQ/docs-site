from datetime import datetime, date, timedelta
import time


def current_timestamp() -> str:
    """Return the current timestamp as a string.

    Eaxmple:
    print(current_timestamp())  # "2025-03-24 12:00:00"
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def days_between(date1: str, date2: str, date_format='%Y-%m-%d') -> int:
    """Return the number of days between two dates.

    Example:
    print(days_between("2025-01-01", "2025-03-24"))  # 82
    """
    d1 = datetime.strptime(date1, date_format)
    d2 = datetime.strptime(date2, date_format)
    return abs((d2 - d1).days)


def add_working_days(start_date: date, num_days: int) -> date:
    """ Calculate the target date by adding a specified number of working days
    (Monday to Friday) to a given start date.

    Args:
        start_date (date): The date from which to start counting.
        num_days (int): The number of working days to add.

    Returns:
       date: The resulting date after adding the working days.

    Example:
        add_working_days(date(2025, 3, 24), 100) # date(2025, 08, 11)
    """
    current_date = start_date
    added_days = 0
    while added_days < num_days:
        current_date += timedelta(days=1)
        # Check if it's a weekday (Monday to Friday)
        if current_date.weekday() < 5:
            added_days += 1
    return current_date


def elapsed_since(start_time: float) -> str:
    """Calculate the elapsed time since the given start time.

    Args:
        start (float): The start time in seconds since the epoch (as returned by time.time())

    Returns:
        str: The elapsed time formatted as HH:MM:SS

    Example:
        start_time = time.time()
        # some code execution
        elapsed = elapsed_since(start_time)
        print(f"Elapsed time: {elapsed}")
    """
    return time.strftime("%H:%M:%S",
                         time.gmtime(time.time() - start_time))

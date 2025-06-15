import re
import datetime


def to_snake_case(text: str) -> str:
    """Convert a string to snake_case.

    Example:
    print(to_snake_case("HelloWorld"))   # hello_world
    """
    return re.sub(r'(?<!^)(?=[A-Z])', '_', text).lower()


def to_camel_case(text: str) -> str:
    """Convert a string to camelCase.

    Example:
    print(to_camel_case("hello_world"))  # helloWorld
    """
    parts = text.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])


def extract_datetime_from_filename(filename: str) -> tuple[datetime.datetime | None, datetime.datetime | None]:
    """Extracts start and end datetime from a filename with a specific pattern.
    Args:
        filename (str): The name of the file.
        Example: "A20230101.2300+0000-0000+0000_1.xml"
    Returns:
        tuple: A tuple containing the start datetime object and the end datetime object.
    """
    # Define the regex pattern to match the datetime format
    pattern = r'[A-Za-z]*(\d{8})\.(\d{4}[+-]\d{4})-(\d{4}[+-]\d{4}).*\.xml'
    # datetime formats
    date_format = "%Y%m%d"
    time_format = "%H%M%z"  # %z is UTC offset in the form [+-]HHMM
    datetime_format = '.'.join([date_format, time_format])
    # init returned datetime objects
    start_datetime_obj, end_datetime_obj = None, None
    try:
        # Use re.match to search for the pattern in the string
        match = re.match(pattern, filename)
        if match:
            # Extract datetime components from the matched groups
            start_date_str = match.group(1)
            start_time_str = match.group(2)
            end_time_str = match.group(3)
            # parse start datetime
            start_datetime_obj = datetime.datetime.strptime(
                '.'.join([start_date_str, start_time_str]), datetime_format)
            # parse end datetime
            end_datetime_obj = datetime.datetime.strptime(
                '.'.join([start_date_str, end_time_str]), datetime_format)
            # If the hour part of the end time is 0,
            # the end date is the next day of the start date
            if end_datetime_obj.hour == 0:
                end_datetime_obj = end_datetime_obj + datetime.timedelta(days=1)

        return (start_datetime_obj, end_datetime_obj)
    except Exception:
        raise ValueError("Error occurred in extracting start and end datetime from the filename: %s", filename)

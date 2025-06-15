import sys
import logging


def create_console_logger():
    """
    Creates and configures a custom logger with a console handler.

    The logger is set to the DEBUG level, and a StreamHandler is added to output
    log messages to the console (stdout). The handler is also configured to use
    the DEBUG level.

    Returns:
        logging.Logger: A configured logger instance.
    """
    logger = logging.getLogger(__name__)
    # Set the level of the logger
    logger.setLevel(logging.DEBUG)
    # Create custom handler. For example this handler is for logging to console
    console_handler = logging.StreamHandler(stream=sys.stdout)
    # Set the level of the handlers (can be different for each handler)
    console_handler.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)

    return logger

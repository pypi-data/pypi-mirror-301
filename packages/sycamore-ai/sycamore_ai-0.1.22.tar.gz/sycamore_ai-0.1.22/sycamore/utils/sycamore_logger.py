import logging
import sys
import time

handler_setup = False


def setup_logger():
    """Setup application logger"""
    global handler_setup
    if handler_setup:
        return
    handler_setup = True
    logger = logging.getLogger("sycamore")
    logger.setLevel(logging.INFO)

    logger_formatter = logging.Formatter("%(name)s - %(levelname)s - %(asctime)s - %(message)s")
    logger_formatter.converter = time.gmtime

    logger_handler = logging.StreamHandler(sys.stdout)
    logger_handler.setLevel(logging.INFO)
    logger_handler.setFormatter(logger_formatter)
    logger.addHandler(logger_handler)


def get_logger():
    """Get an application logger"""
    logger = logging.getLogger("sycamore")
    return logger

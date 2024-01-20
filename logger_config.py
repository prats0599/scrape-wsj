"""
This script configures the logger for the logging.

Author: Muneeb Ur Rehman (muneeb0035@gmail.com)
Date: 18 July 2023
"""
import logging

# This function will set up and return a logger object
def get_logger(logger_name, log_file, level=logging.DEBUG):
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    file_handler = logging.FileHandler(log_file, mode="w")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

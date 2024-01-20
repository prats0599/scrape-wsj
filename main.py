"""
This is the main file which initiates the Scrapper Session.

Author: Muneeb Ur Rehman (muneeb0035@gmail.com)
Date: 18 July 2023
"""

from defaults import LOGGER
from inputs import START_DATE, END_DATE
import scrapper_wrapper


if __name__ == "__main__":
    LOGGER.info("Starting the Scraper")
    scrapper_wrapper.ScrapeData(START_DATE, END_DATE)
    LOGGER.info("Scrapper Finished")

"""
This script sets the default values that can change the
behaviour of the scrapper. 

Author: Muneeb Ur Rehman (muneeb0035@gmail.com)
Date: 18 July 2023
"""
from pathlib import Path
CURRENT_DIR = Path(__file__).resolve().parent

# get logger
from logger_config import get_logger
LOG_FILE = f"{CURRENT_DIR}\\scrapper.log"
LOGGER = get_logger('main_logger', LOG_FILE)

# Out_pur csv file path
CSV_FILE = f'{CURRENT_DIR}/out_csv.csv'

# Base url to get the day data
DATE_URL = "https://www.wsj.com/news/archive/"
# Base WSJ Website
BASE = 'https://www.wsj.com'

# Path to chrome extension file
EXT_FILE = f"{CURRENT_DIR}\\bypass-paywalls-chrome-master"
# Path to the chrome webdriver
CHROME_DRIVER = f"{CURRENT_DIR}\\chromedriver.exe"
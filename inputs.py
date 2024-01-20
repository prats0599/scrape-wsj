"""
This script gets the user inputs.

Author: Muneeb Ur Rehman (muneeb0035@gmail.com)
Date: 18 July 2023
"""

from datetime import date
# --------------- YYY-MM-DD
START_DATE = date(2008,2,1)   # start date 
END_DATE = date(2010,1,1)   # end date

# Multi Threading Options
NUM_THREADS = 25
# Batch/chrome windows to open at the same time
BATCH_SIZE = 8
# Tabs to open per chrome window 
TAB_PER_WIN = 3

# If True it reades the downloaded HTML file
LOCAL_TEST = True
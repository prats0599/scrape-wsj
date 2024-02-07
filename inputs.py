"""
This script gets the user inputs.
"""

from datetime import date
# --------------- YYY-MM-DD
START_DATE = date(2023,10,4)   # start date 
END_DATE = date(2024,1,28)   # end date

# Multi Threading Options
NUM_THREADS = 25
# Batch/chrome windows to open at the same time
BATCH_SIZE = 3
# Tabs to open per chrome window 
TAB_PER_WIN = 5

# If True it reades the downloaded HTML file
LOCAL_TEST = False
"""
This is the scrapper wrapper. It communicates with the scrapper
to retrive the data

Author: Muneeb Ur Rehman (muneeb0035@gmail.com)
Date: 18 July 2023
"""

from defaults import DATE_URL, LOGGER
from inputs import TAB_PER_WIN, BATCH_SIZE, LOCAL_TEST

from datetime import timedelta
import wsj_scrapper


class ScrapeData():

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.Boot()

    def Boot(self):
        new_dic = {}
        LOGGER.info(f"Scraping from {self.start_date} to {self.end_date}")
        for n in range(int ((self.end_date - self.start_date).days)):
            date = str(self.start_date + timedelta(n)).replace('-', '/')
            url = DATE_URL + date
            LOGGER.info(f'Started scraping: {date}')
            wsj_scrapper.get_day_data(url, new_dic)
            LOGGER.info(f"Got {len(new_dic[date])} relevent posts")
            batch_data = self.CreateBatches(new_dic[date])
            LOGGER.debug(f'{len(batch_data)} batches created')
            LOGGER.debug(f'{TAB_PER_WIN} per window')
            wsj_scrapper.get_content(batch_data)
            if LOCAL_TEST:
                break

    def CreateBatches(self, data):
        batch_data = []
        apd_list = []
        coun = 0
        url_li = []
        for url in data:
            if coun == TAB_PER_WIN:
                apd_list.append(url_li)
                url_li = []
                coun = 0
            url_li.append(url)
            coun += 1
        apd_list.append(url_li)

        sub_batch = []
        for lis in apd_list:
            if len(sub_batch) == BATCH_SIZE:
                batch_data.append(sub_batch)
                sub_batch = []
            sub_batch.append(lis)
        batch_data.append(sub_batch)
        return batch_data

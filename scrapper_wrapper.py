"""
This is the scrapper wrapper. It communicates with the scrapper
to retrive the data
"""

from defaults import DATE_URL, LOGGER
from inputs import TAB_PER_WIN, BATCH_SIZE, LOCAL_TEST

from datetime import timedelta
import wsj_scrapper
import time


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

            retries = 0
            while len(new_dic[date])==0 and retries <3:
                time.sleep(5)
                wsj_scrapper.get_day_data(url, new_dic)
                LOGGER.info(f"Retry {retries}: Got {len(new_dic[date])} relevent posts")
                retries += 1
            if len(new_dic[date])>0:
                batch_data = self.CreateBatches(new_dic[date])
                LOGGER.debug(f'{len(batch_data)} batches created')
                LOGGER.debug(f'{TAB_PER_WIN} per window')
                time.sleep(2)
                wsj_scrapper.get_content(batch_data)
            else:
                LOGGER.info(f"No relevent posts found for:{date}")
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

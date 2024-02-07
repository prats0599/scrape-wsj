"""
This is the main scrapper that make calls to the WSJ website
"""
import time
import requests
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor, wait, as_completed
import threading
from defaults import *
from selenium.webdriver.chrome.service import Service

from inputs import NUM_THREADS, LOCAL_TEST

CONTENTS = {}
# Create a lock to synchronize access to the CSV file
csv_lock = threading.Lock()
firefox_ext_lock = threading.Lock()


def write_to_csv(row):
    # Acquire the lock before writing to the CSV file
    with csv_lock:
        with open(CSV_FILE, 'a', newline='', encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(row)
        LOGGER.debug("Data written to CSV file.")


def run_web_driver_session(url):
    init_t = time.time()
    with firefox_ext_lock:
        driver = webdriver.Firefox()#options=PROFILE_OPTIONS)
        driver.install_addon(FIREFOX_EXT)
        time.sleep(2)

    # Minimize the browser window
    driver.minimize_window()
    # LOGGER.info(f"Extracting from:{url}")
    driver.get(url)
    LOGGER.debug(f"Time to start webdriver {time.time() - init_t}")
    return driver


def get_day_data(url, day_dict):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    new_dict = {}
    curr_date = url[-10:]
    # LOGGER.info(curr_date)

    while True:
        time.sleep(0.5)
        if LOCAL_TEST:
            html_file = f"{CURRENT_DIR}\\output.html"
            with open(html_file) as f:
                html_content = f.read()
        else:
            response = requests.get(url, headers=headers)
            html_content = response.text
            # print(html_content)

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")
        # Find all the divs with class "WSJTheme--articleType--34Gt-vdG"
        article_type_divs = soup.find_all("div", class_="WSJTheme--articleType--34Gt-vdG")

        # Find all the divs with class "WSJTheme--headlineText--He1ANr9C"
        headline_spans = soup.find_all("span", class_="WSJTheme--headlineText--He1ANr9C")

        # Extract the data from each occurrence
        for article_type_div, headline_span in zip(article_type_divs, headline_spans):
            articles_type = article_type_div.get_text(strip=True).strip()
            headline = headline_span.get_text(strip=True)
            href = headline_span.find_parent("a")["href"]
            if articles_type in ["Business", "Economy", 'Finance', 'U.S. Economy']:
                new_dict[href] = {"articles_type": articles_type,
                                  "headline": headline, 'date': curr_date}
        
        day_dict[curr_date] = new_dict
        CONTENTS.update(new_dict)
        # Find all <a> elements with the specified class and extract the href attribute
        next_button = soup.find_all("a", class_="WSJTheme--button--12LOad_- typography--sans-serif--1WZesAGA WSJTheme--pagination--3MTI0FnK WSJTheme--next--2r7-j2I8 WSJTheme--secondary--_qx91Q7S")
        if next_button:
            url = next_button[0].get("href")
            if BASE not in url:
                url = f"{BASE}{url}"
            LOGGER.info(f'next_url:{url}')
            if LOCAL_TEST:
                break
        else:
            break
    links = [links for links in new_dict.keys()]
    LOGGER.info(f"links extracted: {links}")


def get_article_content(html_content):
    "Get the HTML content of the tab"
    soup = BeautifulSoup(html_content, 'html.parser')
    p_elements = soup.find_all("p", attrs={"data-type": "paragraph"})
    # Process the extracted <p> elements as needed
    content = str()
    for p in p_elements:
        # Access the content of the <p> element
        content += p.text.strip()
    return content

def get_post_content(urls):
    driver = run_web_driver_session(urls[0])
    # Get the updated page source\

    init_t = time.time()
    for idx, url_1 in enumerate(urls[1:]):
        # Open a new tab
        driver.execute_script("window.open();")
        # Switch to the next tab
        driver.switch_to.window(driver.window_handles[idx + 1])
        driver.get(url_1)
    LOGGER.debug(f"Time to load data in new tabs {time.time() - init_t}")

    # Iterate over each tab
    init_t = time.time()
    for window_handle in driver.window_handles:
        # Switch to the tab
        driver.switch_to.window(window_handle)
        
        # Get the URL of the tab
        url = driver.current_url
        if url.startswith("moz-extension"):
            continue
        
        time.sleep(3)
        html_content = driver.page_source
        content = get_article_content(html_content)        
        retries = 0
        while content == "" and retries<3:
            # driver.get(url)
            driver.refresh()
            time.sleep(5)
            html_content = driver.page_source
            content = get_article_content(html_content)
            retries += 1

        if retries == 3:
            LOGGER.debug(f"Retries failed on URL: {url}")
        elif retries>0:
            LOGGER.info(f"{retries} retries sucessful")
        headline = CONTENTS[url]['headline']
        curr_date = CONTENTS[url]['date']
        data = [url, curr_date, headline, content]
        write_to_csv(data)
    # driver.implicitly_wait(2)
    time.sleep(2)
    driver.quit()
    LOGGER.debug(f"Time to read_page {time.time() - init_t}")


def get_content(data):
    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        # Process each batch sequentially
        for batch in data:
            LOGGER.info(f"Current Batch length: {len(batch)}")
            # Submit tasks to the thread pool for each file in the batch
            futures = [executor.submit(get_post_content, urls) for urls in batch]

            # Wait for all tasks in the batch to complete
            LOGGER.info("Waiting for the jobs to complete")
            wait(futures)
            for future in as_completed(futures):
                future.result()
            LOGGER.info("BATCH COMPLETED")
            if LOCAL_TEST:
                break

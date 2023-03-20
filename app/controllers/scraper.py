# flake8: noqa F501
import time
from celery import Celery
from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import requests
import re
import random
from config import BaseConfig as conf
from app.logger import log


log.set_level(log.DEBUG)
celery = Celery(__name__)
celery.conf.broker_url = conf.REDIS_URL
celery.conf.result_backend = conf.REDIS_URL


@celery.task
def scrape_sites(query):
    REAL_ESTATE_TEXT = "Real Estate Websites by"
    SIERRA_TEXT = "Sierra Interactive"

    links = []

    # chrome_options = Options()
    chrome_options = webdriver.ChromeOptions()
    user_agent = UserAgent()
    user_agent.random
    # chrome_options.add_argument(f"user-agent={user_agent}")
    # chrome_options.add_argument(
    #     "user-agent=Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166"
    # )
    # chrome_options.add_argument('--user-agent="Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166"')
    # chrome_options.add_experimental_option("detach", True)
    browser = webdriver.Chrome(
        executable_path="/home/denys/RealEstate/chromedriver/chromedriver.exr",
        options=chrome_options,
    )
    browser.maximize_window()

    try:
        browser.get(query)

        pages_counter = 0
        while True:
            time.sleep(1)
            results = browser.find_elements(By.CLASS_NAME, "MjjYud")
            for page in results:
                link = page.find_element(By.TAG_NAME, "a").get_attribute("href")
                url_pattern = r"https://[www\.]?[\w\-]+\.[\w\.]+\/"
                matches = re.findall(url_pattern, link)
                url = matches[0]
                contact = url + "contact/"
                page_response = requests.get(contact)
                if page_response.status_code != 200:
                    page_response = requests.get(url)
                print(page_response.status_code, REAL_ESTATE_TEXT in page_response.text)
                if (
                    page_response.status_code == 200
                    and REAL_ESTATE_TEXT in page_response.text
                    and SIERRA_TEXT in page_response.text
                    and "google.com" not in link
                ):

                    filename = (
                        "sierra_file_"
                        + str(random.randint(1000, 9999))
                        + "_"
                        + str(random.randint(1000, 9999))
                        + ".csv"
                    )
                    with open(filename, "w", encoding="utf-8") as file:
                        phones_patterns = [
                            r"\d{3}\s\d{3}\s\d{4}",
                            r"\d{3}-\d{3}-\d{4}",
                            r"\d{3}\.\d{3}\.\d{4}",
                            r"\(\d{3}\).?\d{7}",
                            r"\(\d{3}\).?\d{3}.\d{4}",
                            # r"!\(000\)\s000-0000",
                        ]

                        phones_matches = []
                        for pattern in phones_patterns:
                            single_match = re.findall(pattern, page_response.text)
                            if single_match:
                                phones_matches.extend(single_match)

                        phones_cleaned = [
                            x for x in phones_matches if x != "(000) 000-0000"
                        ]
                        unique_phones = set(phones_cleaned)
                        phones_csv = ",".join(unique_phones)

                        email_pattern = r"[\w_.]+@[a-z\-]+\.[a-z\.]{2,}"

                        mails_match = re.findall(email_pattern, page_response.text)
                        mails_cleaned = [
                            x for x in mails_match if x != "name@website.com"
                        ]

                        unique_mails = set(mails_cleaned)
                        mails_csv = ",".join(unique_mails)
                        csv = (
                            "URL,"
                            + "Contacts\n"
                            + url
                            + ","
                            + mails_csv
                            + ","
                            + phones_csv
                        )
                        file.write(csv)

                    links.append(url)

            pages_counter += 1
            next_button = browser.find_element(By.ID, "pnnext")
            if pages_counter == 2 or not next_button:
                break
            next_button.click()
        print(links)
        print(len(links))
    except Exception as e:
        print(e)
    finally:
        browser.close()
        browser.quit()

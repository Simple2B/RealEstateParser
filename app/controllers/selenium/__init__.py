import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import requests
import re
import random
from config import BaseConfig as conf
from app.logger import log


def scrape(query: str):
    log(log.INFO, "run controllers.scrape()")
    log(log.INFO, "query: [%s]", conf.SEARH_QUERY)
    REAL_ESTATE_TEXT = "Real Estate Websites by"
    SIERRA_TEXT = "Sierra Interactive"

    links = []

    # chrome_options = Options()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    user_agent = UserAgent()
    user_agent.random
    chrome_options.add_argument(f"user-agent={user_agent}")
    browser = webdriver.Chrome(
        executable_path="app/controllers/selenium/webdriver/chromedriver",
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
                        csv = f"URL,Contacts\n{url},{mails_csv},{phones_csv}"
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

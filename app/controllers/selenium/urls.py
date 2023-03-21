import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import requests
import re
from config import BaseConfig as conf
from app.models import Site
from app.logger import log


def scrape(query: str):
    log(log.INFO, "run controllers.scrape()")
    log(log.INFO, "query: [%s]", conf.SEARH_QUERY)
    REAL_ESTATE_TEXT = "Real Estate Websites by"
    SIERRA_TEXT = "Sierra Interactive"

    urls = []

    chrome_options = webdriver.FirefoxOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    user_agent = UserAgent()
    user_agent.random
    chrome_options.add_argument(f"user-agent={user_agent}")
    browser = webdriver.Firefox(
        executable_path="app/controllers/selenium/webdriver/geckodriver",
        options=chrome_options,
    )
    log(log.INFO, "UserAgent: [%s]", user_agent)

    try:
        log(log.INFO, "try")
        browser.get(query)
        log(log.INFO, "browser.get(query): [%s]", query)

        pages_counter = 0
        while True:
            time.sleep(1)
            results = browser.find_elements(By.CLASS_NAME, "MjjYud")
            for page in results:
                link = page.find_element(By.TAG_NAME, "a").get_attribute("href")
                url_pattern = r"https://[www\.]?[\w\-]+\.[\w\.]+\/"
                matches = re.findall(url_pattern, link)
                url = matches[0] if matches else link
                page_response = requests.get(url)
                log(
                    log.INFO,
                    "page_response.status_code: %s, REAL_ESTATE_TEXT: %s",
                    page_response.status_code,
                    REAL_ESTATE_TEXT in page_response.text,
                )
                if (
                    page_response.status_code == 200
                    and REAL_ESTATE_TEXT in page_response.text
                    and SIERRA_TEXT in page_response.text
                    and "google.com" not in link
                ):
                    current_site: Site = Site.query.filter_by(url=url).first()
                    if not current_site:
                        Site(url=url).save()
                    urls.append(url)

            pages_counter += 1
            next_button = browser.find_element(By.ID, "pnnext")
            if pages_counter == 17 or not next_button:
                break

            new_page = next_button.get_attribute("href")
            browser.get(new_page)
        log(log.INFO, "urls just saved: [%d]", len(urls))
    except Exception as e:
        print("Exception: ", e)
    finally:
        browser.close()
        browser.quit()

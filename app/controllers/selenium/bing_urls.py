import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import requests
import re
from config import BaseConfig as conf
from app.models import Site
from app.logger import log


def set_browser():
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
    return browser


def scrape(query: str):
    log(log.INFO, "run controllers.scrape()")
    log(log.INFO, "query: [%s]", conf.SEARH_QUERY)
    REAL_ESTATE_TEXT = "Real Estate Websites by"
    SIERRA_TEXT = "Sierra Interactive"

    urls = []

    browser = set_browser()

    try:
        log(log.INFO, "try")
        browser.get(query)
        log(log.INFO, "browser.get(query): [%s]", query)

        pages_counter = 0
        while True:
            time.sleep(1)
            results = browser.find_elements(By.CLASS_NAME, "b_algo")
            for page in results:
                inner_div = page.find_element(By.CLASS_NAME, "b_title")
                h2 = inner_div.find_element(By.TAG_NAME, "h2")
                link = h2.find_element(By.TAG_NAME, "a").get_attribute("href")
                url_pattern = r"https://[www\.]?[\w\-]+\.[\w\.]+\/"
                matches = re.findall(url_pattern, link)
                url = matches[0] if matches else link
                if "google.com" in url:
                    continue
                current_site: Site = Site.query.filter_by(url=url).first()
                if current_site:
                    continue
                try:
                    page_response = requests.get(url, timeout=15)
                except Exception:
                    continue
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
                ):
                    new_site = Site(url=url)
                    new_site.save()
                    urls.append(url)
                    log(log.INFO, "[%d] Saved URL: %s", new_site.id, url)

            pages_counter += 1
            log(log.INFO, "Pages parsed: %d", pages_counter)
            try:
                next_button = browser.find_element(By.CLASS_NAME, "sb_pagN")
            except Exception:
                log(log.ERROR, "No next button")

            if pages_counter >= conf.MAX_PAGES_AMOUNT:
                log(log.INFO, "Max pages reached")
                break

            new_page = next_button.get_attribute("href")
            browser.get(new_page)
        log(log.INFO, "urls just saved: [%d]", len(urls))
    except Exception as e:
        log(log.ERROR, "Error: %s", e)
    finally:
        browser.close()
        browser.quit()

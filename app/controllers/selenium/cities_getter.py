import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from app.models import City
from app.logger import log

COMMERCE_CHAMBER_URL = "https://www.officialusa.com/stateguides/chambers/"


def set_browser():
    chrome_options = webdriver.FirefoxOptions()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    user_agent = UserAgent()
    user_agent.random
    chrome_options.add_argument(f"user-agent={user_agent}")
    browser = webdriver.Firefox(
        executable_path="app\controllers\selenium\webdriver\geckodriver.exe",
        options=chrome_options,
    )
    log(log.INFO, "UserAgent: [%s]", user_agent)
    return browser


def get_cities():
    log(log.INFO, "run get_cities()")

    urls = []

    browser = set_browser()

    try:
        log(log.INFO, "try")
        browser.get(COMMERCE_CHAMBER_URL)
        log(log.INFO, "browser.get(%s)", COMMERCE_CHAMBER_URL)

        time.sleep(3)

        results = browser.find_elements(By.TAG_NAME, "a")
        for page in results:
            link = page.get_attribute("href")
            if not link:
                continue
            urls.append(link)

        print(urls)

    except Exception as e:
        log(log.ERROR, "Error: %s", e)
    finally:
        browser.close()
        browser.quit()

import time
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from app.models import City
from app.logger import log

COMMERCE_CHAMBER_URL = "https://www.officialusa.com/stateguides/chambers/"

CHAMBERS = [
    "https://www.officialusa.com/stateguides/chambers/alaska.html",
    "https://www.officialusa.com/stateguides/chambers/alabama.html",
    "https://www.officialusa.com/stateguides/chambers/arizona.html",
    "https://www.officialusa.com/stateguides/chambers/arkansas.html",
    "https://www.officialusa.com/stateguides/chambers/california.html",
    "https://www.officialusa.com/stateguides/chambers/colorado.html",
    "https://www.officialusa.com/stateguides/chambers/connecticut.html",
    "https://www.officialusa.com/stateguides/chambers/delaware.html",
    "https://www.officialusa.com/stateguides/chambers/florida.html",
    "https://www.officialusa.com/stateguides/chambers/georgia.html",
    "https://www.officialusa.com/stateguides/chambers/hawaii.html",
    "https://www.officialusa.com/stateguides/chambers/idaho.html",
    "https://www.officialusa.com/stateguides/chambers/illinois.html",
    "https://www.officialusa.com/stateguides/chambers/indiana.html",
    "https://www.officialusa.com/stateguides/chambers/iowa.html",
    "https://www.officialusa.com/stateguides/chambers/kansas.html",
    "https://www.officialusa.com/stateguides/chambers/kentucky.html",
    "https://www.officialusa.com/stateguides/chambers/louisiana.html",
    "https://www.officialusa.com/stateguides/chambers/maine.html",
    "https://www.officialusa.com/stateguides/chambers/maryland.html",
    "https://www.officialusa.com/stateguides/chambers/massachusetts.html",
    "https://www.officialusa.com/stateguides/chambers/michigan.html",
    "https://www.officialusa.com/stateguides/chambers/minnesota.html",
    "https://www.officialusa.com/stateguides/chambers/mississippi.html",
    "https://www.officialusa.com/stateguides/chambers/missouri.html",
    "https://www.officialusa.com/stateguides/chambers/montana.html",
    "https://www.officialusa.com/stateguides/chambers/newjersey.html",
    "https://www.officialusa.com/stateguides/chambers/newmexico.html",
    "https://www.officialusa.com/stateguides/chambers/newyork.html",
    "https://www.officialusa.com/stateguides/chambers/northcarolina.html",
    "https://www.officialusa.com/stateguides/chambers/northdakota.html",
    "https://www.officialusa.com/stateguides/chambers/ohio.html",
    "https://www.officialusa.com/stateguides/chambers/oklahoma.html",
    "https://www.officialusa.com/stateguides/chambers/oregon.html",
    "https://www.officialusa.com/stateguides/chambers/pennsylvania.html",
    "https://www.officialusa.com/stateguides/chambers/rhodeisland.html",
    "https://www.officialusa.com/stateguides/chambers/southcarolina.html",
    "https://www.officialusa.com/stateguides/chambers/southdakota.html",
    "https://www.officialusa.com/stateguides/chambers/tennessee.html",
    "https://www.officialusa.com/stateguides/chambers/texas.html",
    "https://www.officialusa.com/stateguides/chambers/utah.html",
    "https://www.officialusa.com/stateguides/chambers/vermont.html",
    "https://www.officialusa.com/stateguides/chambers/virginia.html",
    "https://www.officialusa.com/stateguides/chambers/washington.html",
    "https://www.officialusa.com/stateguides/chambers/westvirginia.html",
    "https://www.officialusa.com/stateguides/chambers/wisconsin.html",
    "https://www.officialusa.com/stateguides/chambers/wyoming.html",
]


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
    log(log.INFO, "CHAMBERS len: %d", len(CHAMBERS))
    log(log.INFO, "run get_cities()")

    pattern = re.compile(r"\/([\w]+)\.html")

    browser = set_browser()

    for link in CHAMBERS:
        state = re.search(pattern, link).group(1)

        browser.get(link)
        log(log.INFO, "browser.get(%s)", link)

        time.sleep(3)
        results = browser.find_elements(By.TAG_NAME, "tr")
        for item in results:
            try:
                city = item.find_element(By.TAG_NAME, "td").get_attribute("innerHTML")
                City(name=city, state=state).save()
            except:
                continue

import random
import time
import us
import geonamescache
from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import requests
import re
from config import BaseConfig as conf
from app.models import Site, Location, URL, City
from app.logger import log


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


def scrape(query: str, location_name):
    log(log.INFO, "run controllers.scrape()")
    log(log.INFO, "query: [%s]", query)
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
            while "captcha" in browser.page_source:
                log(log.WARNING, "CAPTCHA DETECTED!")
                time.sleep(3)
            results = browser.find_elements(By.TAG_NAME, "a")
            for page in results:
                link = page.get_attribute("href")
                if not link:
                    continue
                url_pattern = r"https://[www\.]?[\w\-]+\.[a-z]{2,3}"
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
                elif page_response.status_code == 200:
                    other_site = URL(url=url)
                    other_site.save()

            pages_counter += 1
            log(log.INFO, "Pages parsed: %d", pages_counter)
            try:
                next_button = browser.find_element(By.ID, "pnnext")
            except Exception:
                try:
                    log(log.ERROR, "No next button")
                    # location = Location(name=location_name)
                    # location.save()
                    next_button = browser.find_element(By.TAG_NAME, "i")
                except Exception:
                    log(log.ERROR, "No extended results")

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


def scrape_states():
    for state in us.states.STATES:
        state: us.states.State = state
        query_str = "+".join([state.abbr, conf.SEARCH_STR])
        query = conf.BASE_GOOGLE_GET.format(query_str)
        scrape(query)
        # state
    pass


def scrape_cities():
    gc = geonamescache.GeonamesCache()
    cities = gc.get_cities()
    us_cities = []
    for city in cities:
        if cities[city]["countrycode"] == "US":
            us_cities.append(cities[city]["name"].replace(" ", "+"))
    random.shuffle(us_cities)
    for index, us_city in enumerate(us_cities):
        query_str = "+".join([us_city, conf.SEARCH_STR])
        query = conf.BASE_GOOGLE_GET.format(query_str)
        log(log.INFO, "-------City %d of %d: %s-------", index, len(us_cities), us_city)
        if not Location.query.filter_by(name=us_city).first():
            scrape(query, us_city)


def scrape_counties():
    gc = geonamescache.GeonamesCache()
    counties = gc.get_us_counties()
    random.shuffle(counties)
    for index, county in enumerate(counties):
        query_str = "+".join([county["name"].replace(" ", "+"), conf.SEARCH_STR])
        query = conf.BASE_GOOGLE_GET.format(query_str)
        log(log.INFO, "-------County %d of %d: %s-------", index, len(counties), county)
        if not Location.query.filter_by(name=county["name"]).first():
            scrape(query, county["name"])


def scrape_db_cities():
    page = 1
    CITIES_PER_PAGE = 100
    cities: list[City] = City.query.paginate(page=page, per_page=CITIES_PER_PAGE)
    pages_amount = cities.total // CITIES_PER_PAGE
    for page in range(1, pages_amount):
        log(log.INFO, "-------Checking page %d of %d-------", page, pages_amount)
        cities: list[City] = City.query.paginate(page=page, per_page=CITIES_PER_PAGE)
        for city in cities:
            log(log.INFO, "Checking city %d: %s, %s", city.id, city.name, city.state)
            query_str = "+".join([city.name, conf.SEARCH_STR])
            query = conf.BASE_GOOGLE_GET.format(query_str)
            scrape(query, city.name)

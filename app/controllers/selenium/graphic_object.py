import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from app.models import URL, Image
from app.logger import log
from .urls import set_browser

URLS = [
    "http://www.vikrampal.com/",
    "http://www.homesalesco.com/",
    "https://www.iowarealty.com/",
    "https://www.thelindseybartleyteam.com/",
]

OBJECT_TEXT_1 = "widgetbe.com/agent"
OBJECT_TEXT_2 = "WidgetTrackerObject"


def check_graphic_object():
    browser = set_browser()
    foundings = []

    page = 1
    SITES_PER_PAGE = 100
    sites: list[URL] = URL.query.paginate(page=page, per_page=SITES_PER_PAGE)
    pages_amount = sites.total // SITES_PER_PAGE
    for page in range(2, pages_amount):
        log(log.INFO, "-------Checking page %d of %d-------", page, pages_amount)
        sites: list[URL] = URL.query.paginate(page=page, per_page=SITES_PER_PAGE)
        for site in sites:
            url_pattern = r"https://[www\.]?[\w\-]+\.[a-z]{2,3}"
            matches = re.findall(url_pattern, site.url)
            url = matches[0] if matches else site.url
            log(log.INFO, "Checking url: %s", site.url)
            try:
                browser.get(url)
            except Exception:
                continue

            if (
                OBJECT_TEXT_1 in browser.page_source
                and OBJECT_TEXT_2 in browser.page_source
            ):
                log(log.INFO, "Text found in url: %s", url)
                saved: Image = Image.query.filter_by(url=url).first()
                if saved:
                    continue
                Image(url=url).save()
                log(log.INFO, "Site saved: %s", url)
                foundings.append(url)
                continue

            results = browser.find_elements(By.TAG_NAME, "script")
            for r in results:
                try:
                    link = r.get_attribute("href")
                except Exception as e:
                    log(log.ERROR, "No attribute href: %s", e)
                    continue
                if not link:
                    continue
                try:
                    response = requests.get(link, timeout=5)
                except ConnectionError:
                    log(log.ERROR, "ConnectionError")
                    continue
                if response.status_code == 200 and (
                    OBJECT_TEXT_1 in response.text or OBJECT_TEXT_2 in response.text
                ):
                    log(log.INFO, "Text found")
                    saved: Image = Image.query.filter_by(url=site.url).first()
                    if saved:
                        continue
                    Image(url=site.url).save()
                    log(log.INFO, "Site saved: %s", site.url)
                    foundings.append(site)
        log(log.INFO, "Page %d. Currently found: %d", page, len(foundings))
    log(log.INFO, "Foundings %s: ", foundings)


def testing_image_sites():
    browser = set_browser()
    foundings = []

    for url in URLS:
        browser.get(url)
        if (
            OBJECT_TEXT_1 in browser.page_source
            and OBJECT_TEXT_2 in browser.page_source
        ):
            log(log.INFO, "Text found in url: %s", url)
            foundings.append(url)
            continue

        results = browser.find_elements(By.TAG_NAME, "script")
        for index, r in enumerate(results):
            log(log.INFO, "result %d", index)
            try:
                link = r.get_attribute("href")
            except:
                continue
            if not link:
                continue
            try:
                response = requests.get(link, timeout=5)
            except ConnectionError:
                log(log.ERROR, "ConnectionError")
                continue
            if response.status_code == 200 and (
                OBJECT_TEXT_1 in response.text and OBJECT_TEXT_2 in response.text
            ):
                log(log.INFO, "Text found in url: %s", url)
                foundings.append(url)
            log(log.INFO, "Currently found: %d", len(foundings))
    log(log.INFO, "Foundings %s: ", foundings)

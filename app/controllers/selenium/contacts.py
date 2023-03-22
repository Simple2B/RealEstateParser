import requests
import re
from app.models import Site, Email, Phone
from app.logger import log

TEL_RE = re.compile(r"tel:(?P<num>\+\d{11})")

PHONE_PATTERNS = [
    r"\d{3}\s\d{3}\s\d{4}",
    r"\d{3}-\d{3}-\d{4}",
    r"\d{3}\.\d{3}\.\d{4}",
    r"\(\d{3}\).?\d{7}",
    r"\(\d{3}\).?\d{3}.\d{4}",
]
PHONE_RE = [re.compile(p) for p in PHONE_PATTERNS]


def get_emails(sites):
    for site in sites:
        log(log.INFO, "URL: %s", site.url)
        response = requests.get(site.url)
        if response.status_code == 200:
            # Parse emails
            email_pattern = r"[\w_.]+@[\w\-]+\.[a-z\.]{2,}"
            mails_match = re.findall(email_pattern, response.text)
            mails_cleaned = [x for x in mails_match if x != "name@website.com"]
            unique_mails = set(mails_cleaned)
            for email_address in unique_mails:
                email: Email = Email.query.filter_by(email=email_address).first()
                if not email:
                    log(log.INFO, "Saving email [%s] to site [%s]", email_address, site)
                    email: Email = Email(email=email_address)
                else:
                    log(
                        log.INFO,
                        "Email [%s] already exists adding site relationship [%s]",
                        email_address,
                        site,
                    )
                email.sites.append(site)
                email.save()


def get_phones(sites):
    for site in sites:
        log(log.INFO, "URL: %s", site.url)
        response = requests.get(site.url)
        if response.status_code == 200:
            phones_matches = []
            phones_cleaned = []

            tel_found: list[str] = TEL_RE.findall(response.text)

            if tel_found:
                phones_cleaned = tel_found
            else:
                for r in PHONE_RE:
                    single_match: list[str] = r.findall(response.text)
                    if single_match:
                        phones_matches.extend(single_match)
                        # break # ??

                phones_cleaned = [x for x in phones_matches if x != "(000) 000-0000"]

            unique_phones = set(phones_cleaned)
            for phone_number in unique_phones:
                phone: Phone = Phone.query.filter_by(number=phone_number).first()
                if not phone:
                    log(
                        log.INFO,
                        "Saving phone_number [%s] to site [%s]",
                        phone_number,
                        site,
                    )
                    phone: Phone = Phone(number=phone_number)
                else:
                    log(
                        log.INFO,
                        "Phone number [%s] already exists adding site relationship [%s]",
                        phone_number,
                        site,
                    )
                phone.sites.append(site)
                phone.save()


def scrape_contacts():
    log(log.INFO, "Scraping contacts using URLs database")
    no_email_sites = Site.query.filter(Site.emails == None).all()  # noqa E711
    get_emails(no_email_sites)
    no_phone_sites = Site.query.filter(Site.phones == None).all()  # noqa E711
    get_phones(no_phone_sites)

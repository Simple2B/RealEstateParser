import requests
import re
from app.models import Site, Email, Phone
from app.logger import log


def scrape_contacts():
    log(log.INFO, "Scraping contacts using URLs database")
    sites = Site.query.filter()
    for site in sites:
        log(log.INFO, "URL: %s", site.url)
        response = requests.get(site.url)
        if response.status_code == 200:
            # Parse phones
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
                single_match = re.findall(pattern, response.text)
                if single_match:
                    phones_matches.extend(single_match)

            phones_cleaned = [x for x in phones_matches if x != "(000) 000-0000"]
            unique_phones = set(phones_cleaned)
            for phone_number in unique_phones:
                log(
                    log.INFO,
                    "Saving phone_number [%s] to site [%s]",
                    phone_number,
                    site,
                )
                phone: Phone = Phone(number=phone_number)
                phone.sites.append(site)
                phone.save()

            # Parse emails
            email_pattern = r"[\w_.]+@[\w\-]+\.[a-z\.]{2,}"
            mails_match = re.findall(email_pattern, response.text)
            mails_cleaned = [x for x in mails_match if x != "name@website.com"]
            unique_mails = set(mails_cleaned)
            for email_address in unique_mails:
                log(log.INFO, "Saving email [%s] to site [%s]", email_address, site)
                email: Email = Email(email=email_address)
                email.sites.append(site)
                email.save()

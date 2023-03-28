import requests
from app.models import URL, Image
from app.logger import log

OBJECT_TEXT_1 = "&lt;!-- begin Widget Tracker Code --&gt;"
OBJECT_TEXT_2 = "&lt;script&gt;"
OBJECT_TEXT_3 = "(function(w,i,d,g,e,t){w[&quot;WidgetTrackerObject&quot;]=g;"


def check_graphic_object():
    foundings = []

    page = 1
    SITES_PER_PAGE = 100
    sites: list[URL] = URL.query.paginate(page=page, per_page=SITES_PER_PAGE)
    pages_amount = sites.total // SITES_PER_PAGE
    for page in range(43, pages_amount):
        log(log.INFO, "-------Checking page %d of %d-------", page, pages_amount)
        sites: list[URL] = URL.query.paginate(page=page, per_page=SITES_PER_PAGE)
        for site in sites:
            log(log.INFO, "Checking url: %s", site.url)
            try:
                response = requests.get(site.url, timeout=10)
            except Exception:
                continue
            if response.status_code == 200 and OBJECT_TEXT_1 in response.text:
                log(log.INFO, "Text found: %s", OBJECT_TEXT_1)
                saved: Image = Image.query.filter_by(url=site.url).first()
                if saved:
                    continue
                Image(url=site.url).save()
                log(log.INFO, "Site saved: %s", site.url)
                foundings.append(site)
        log(log.INFO, "Page %d. Currently found: %d", page, len(foundings))
    log(log.INFO, "Foundings %d: ", foundings)

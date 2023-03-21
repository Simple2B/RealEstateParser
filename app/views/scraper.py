import io
import csv
from datetime import datetime
from flask import request, render_template, Blueprint, send_file
from flask_login import login_required
from app.models import Site
from app.logger import log

scraping_blueprint = Blueprint("scraping", __name__)


@scraping_blueprint.route("/scraping", methods=["GET", "POST"])
@login_required
def scraping():
    sites_amount: Site = Site.query.count()
    log(log.INFO, "request.method: [%s]", request.method)
    return render_template("scraping.html", sites_amount=sites_amount)


@scraping_blueprint.route("/download", methods=["GET", "POST"])
@login_required
def download():
    sites = Site.query.all()
    with io.StringIO() as proxy:
        writer = csv.writer(proxy)
        row = [
            "№",
            "URL",
            "Emails",
            "Phones",
        ]
        writer.writerow(row)
        for index, site in enumerate(sites):
            emails = [x.email for x in site.emails]
            phones = [x.number for x in site.phones]
            row = [
                f"{index + 1}",
                site.url,
                " ".join(emails),
                "; ".join(phones),
            ]
            writer.writerow(row)

        # Creating the byteIO object from the StringIO Object
        mem = io.BytesIO()
        mem.write(proxy.getvalue().encode("utf-8"))
        mem.seek(0)

    now = datetime.now()
    return send_file(
        mem,
        as_attachment=True,
        download_name=f"contacts_{now.strftime('%Y-%m-%d-%H-%M-%S')}.csv",
        mimetype="text/csv",
        max_age=0,
        last_modified=now,
    )

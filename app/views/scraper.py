from flask import request, render_template, Blueprint, send_file
from app.models import Site
from app.logger import log

scraping_blueprint = Blueprint("scraping", __name__)


@scraping_blueprint.route("/scraping", methods=["GET", "POST"])
def scraping():
    sites_amount: Site = Site.query.count()
    # if request.method == "POST":
    #     log(log.INFO, "request.method: [%s]", request.method)
    log(log.INFO, "request.method: [%s]", request.method)
    return render_template("scraping.html", sites_amount=sites_amount)


@scraping_blueprint.route("/download", methods=["GET", "POST"])
def download():
    file_path = "contacts.csv"
    sites = Site.query.all()
    file_content = "id,url\n"
    for site in sites:
        file_content += f"{str(site.id)},{site.url}\n"
    with open(file_path, "w") as file:
        file.write(file_content)
    return send_file(file_path, as_attachment=True)

from flask import request, render_template, Blueprint
from app.controllers.scraper import scrape_sites
from config import BaseConfig as conf

scraping_blueprint = Blueprint("scraping", __name__)


@scraping_blueprint.route("/scraping", methods=["GET", "POST"])
def scraping():
    if request.method == "POST":
        query = conf.SEARH_QUERY
        print(request.method)
        scrape_sites(query)
    return render_template("scraping.html")

from flask import render_template, Blueprint

scraping_blueprint = Blueprint("scraping", __name__)


@scraping_blueprint.route("/scraping")
def scraping():
    return render_template("scraping.html")

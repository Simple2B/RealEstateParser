#!/user/bin/env python
import click
from app import create_app, db, models, forms
from config import BaseConfig as conf

app = create_app()


# flask cli context setup
@app.shell_context_processor
def get_context():
    """Objects exposed here will be automatically available from the shell."""
    return dict(app=app, db=db, m=models, f=forms, conf=conf)


@app.cli.command()
def create_admin():
    """Creates an admin user."""
    from config import BaseConfig as cfg

    models.User(
        username=cfg.ADMIN_NAME,
        password=cfg.ADMIN_PASS,
        email=cfg.ADMIN_EMAIL,
    ).save()

    print("Admin user has been created!")


@app.cli.command()
@click.argument("query", default=conf.SEARCH_QUERY)
def run_scraper(query: str = conf.SEARCH_QUERY):
    """Runs selenium code."""
    from app.controllers.selenium import scrape

    scrape(query)


@app.cli.command()
def run_scrape_states():
    """Runs selenium code."""
    from app.controllers.selenium import scrape_states

    scrape_states()


@app.cli.command()
def run_scrape_cities():
    """Runs selenium code."""
    from app.controllers.selenium import scrape_cities

    scrape_cities()


@app.cli.command()
def run_scrape_counties():
    """Runs selenium code."""
    from app.controllers.selenium import scrape_counties

    scrape_counties()


@app.cli.command()
def run_scrape_db_cities():
    """Runs selenium code."""
    from app.controllers.selenium import scrape_db_cities

    scrape_db_cities()


@app.cli.command()
def get_contacts():
    """Goes through sites in db and gets emails and phones for each site"""
    from app.controllers.selenium import scrape_contacts

    scrape_contacts()


@app.cli.command()
def check_image_object():
    """Goes through sites in db and gets emails and phones for each site"""
    from app.controllers.selenium import check_graphic_object

    check_graphic_object()


@app.cli.command()
def testing_image_search():
    """Goes through sites in db and gets emails and phones for each site"""
    from app.controllers.selenium import testing_image_sites

    testing_image_sites()


@app.cli.command()
def see_contacts():
    """Gets sites' contacts"""
    from app.models import Site

    sites: Site = Site.query.all()
    print(len(sites))


if __name__ == "__main__":
    app.run()

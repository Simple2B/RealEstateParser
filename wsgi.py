#!/user/bin/env python
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
def run_scraper(query: str = conf.SEARH_QUERY):
    """Runs selenium code."""
    from app.controllers.selenium import scrape

    scrape(query)


if __name__ == "__main__":
    app.run()

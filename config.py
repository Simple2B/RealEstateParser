import os

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


class BaseConfig(object):
    """Base configuration."""

    APP_NAME = "Simple2Scrape"
    DEBUG_TB_ENABLED = False
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "Ensure you set a secret key, this is important!",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False

    # Mail config
    MAIL_SERVER = os.getenv("MAIL_SERVER", "mail.simple2b.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", "465"))
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "!setup in .env!")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "!setup in .env!")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "!setup in .env!")
    ADMIN_NAME = os.getenv("ADMIN_NAME", "admin")
    ADMIN_PASS = os.getenv("ADMIN_NAME", "admin")
    ADMIN_EMAIL = os.getenv("ADMIN_NAME", "admin@simple2b.net")
    REDIS_URL = os.getenv("REDIS_URL", "")
    SEARCH_QUERY = os.getenv(
        "SEARCH_QUERY",
        "Real+Estate+Websites+by+Sierra+Interactive",
    )
    MAX_PAGES_AMOUNT = int(os.getenv("MAX_PAGES_AMOUNT", "100"))
    SEARCH_STR = os.getenv("SEARCH_STR", "Real+Estate+Websites+by+Sierra+Interactive")

    BASE_GOOGLE_GET = os.getenv(
        "BASE_GOOGLE_GET",
        "https://www.google.com/search?q={}",
    )

    @staticmethod
    def configure(app):
        # Implement this method to do further configuration on your app.
        pass


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEVEL_DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "database-devel.sqlite3"),
    )


class TestingConfig(BaseConfig):
    """Testing configuration."""

    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TEST_DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "database-test.sqlite3"),
    )


class ProductionConfig(BaseConfig):
    """Production configuration."""

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "database.sqlite3")
    )
    WTF_CSRF_ENABLED = True


config = dict(
    development=DevelopmentConfig, testing=TestingConfig, production=ProductionConfig
)

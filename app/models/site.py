# flake8: noqa F401
import enum
from datetime import datetime
from sqlalchemy import Enum
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app import db
from app.models.utils import ModelMixin
from .phone import Phone
from .email import Email
from .assotiation import phone_site, email_site


class Site(db.Model, ModelMixin):
    class State(enum.Enum):
        NEW = "new"
        PARSED = "parsed"
        VERIFIED = "verified"

    __tablename__ = "sites"

    id: Mapped[int] = mapped_column(primary_key=True)
    url = db.Column(db.String(256), unique=True, nullable=False)
    state = db.Column(Enum(State), default=State.NEW)
    created_at = db.Column(db.DateTime, default=datetime.now)
    parsed_at = db.Column(db.DateTime, default=datetime.max)

    phones: Mapped[list[Phone]] = relationship(
        "Phone",
        secondary=phone_site,
        backref="phones",
    )
    emails: Mapped[list[Email]] = relationship(
        "Email",
        secondary=email_site,
        backref="emails",
    )

    def __repr__(self):
        return f"<{self.id}:{self.url}: {self.state}, {self.emails}, {self.phones}>"

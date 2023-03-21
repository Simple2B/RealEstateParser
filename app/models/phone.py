from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app import db
from app.models.utils import ModelMixin
from .assotiation import phone_site


class Phone(db.Model, ModelMixin):

    __tablename__ = "phones"

    id: Mapped[int] = mapped_column(primary_key=True)
    number = db.Column(db.String(256), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    sites = relationship(
        "Site",
        secondary=phone_site,
        backref="sites",
    )

    def __repr__(self):
        return f"<{self.id}:{self.number}>"

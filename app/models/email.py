from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app import db
from app.models.utils import ModelMixin
from .assotiation import email_site


class Email(db.Model, ModelMixin):

    __tablename__ = "emails"

    id: Mapped[int] = mapped_column(primary_key=True)
    email = db.Column(db.String(256), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    sites = relationship("Site", secondary=email_site, backref="related_sites")

    def __repr__(self):
        return f"<{self.id}:{self.email}>"

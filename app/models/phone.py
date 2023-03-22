from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app import db
from app.models.utils import ModelMixin


class Phone(db.Model, ModelMixin):

    __tablename__ = "phones"

    id: Mapped[int] = mapped_column(primary_key=True)
    number = db.Column(db.String(256), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<{self.id}:{self.number}>"

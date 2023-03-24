# flake8: noqa F401
from datetime import datetime
from app import db
from app.models.utils import ModelMixin


class URL(db.Model, ModelMixin):

    __tablename__ = "urls"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(256), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"<{self.id}:{self.url}:{self.created_at}>"

from datetime import datetime
from app import db
from app.models.utils import ModelMixin


class City(db.Model, ModelMixin):

    __tablename__ = "cities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    state = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"<{self.id}:{self.name}:{self.state}:{self.created_at}>"

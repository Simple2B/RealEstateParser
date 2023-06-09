from datetime import datetime
from uuid import uuid4

from flask_login import UserMixin, AnonymousUserMixin
from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models.utils import ModelMixin
from app.logger import log


def gen_password_reset_id() -> str:
    return str(uuid4())


class User(db.Model, UserMixin, ModelMixin):

    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    activated = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    unique_id = db.Column(db.String(36), default=gen_password_reset_id)

    @hybrid_property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @classmethod
    def authenticate(cls, user_id, password):
        user = cls.query.filter(
            db.or_(
                func.lower(cls.username) == func.lower(user_id),
                func.lower(cls.email) == func.lower(user_id),
            )
        ).first()
        if not user:
            log(log.ERROR, "Unknown user: [%s]", user_id)
            return

        if not check_password_hash(user.password, password):
            log(log.ERROR, "Wrong password [%s] for user: [%s]", password, user_id)
            return

        return user

    def __repr__(self):
        return f"<User: {self.username}>"


class AnonymousUser(AnonymousUserMixin):
    pass

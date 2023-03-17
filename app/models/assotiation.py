from __future__ import annotations

from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from app import db


class Base(DeclarativeBase):
    pass


phone_site = Table(
    "phone_site",
    Base.metadata,
    Column("site_id", ForeignKey("sites.id")),
    Column("phone_id", ForeignKey("phones.id")),
)


class PhoneSite(db.Model):

    __tablename__ = "phone_site"

    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(ForeignKey("sites.id"))
    phone_id = db.Column(ForeignKey("phones.id"))


email_site = Table(
    "email_site",
    Base.metadata,
    Column("site_id", ForeignKey("sites.id")),
    Column("email_id", ForeignKey("emails.id")),
)


class EmailSite(db.Model):

    __tablename__ = "email_site"

    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(ForeignKey("sites.id"))
    email_id = db.Column(ForeignKey("emails.id"))

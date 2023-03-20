from __future__ import annotations

from app import db


phone_site = db.Table(
    "phone_site",
    db.Column("site_id", db.ForeignKey("sites.id")),
    db.Column("phone_id", db.ForeignKey("phones.id")),
)


email_site = db.Table(
    "email_site",
    db.Column("site_id", db.ForeignKey("sites.id")),
    db.Column("email_id", db.ForeignKey("emails.id")),
)

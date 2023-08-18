import uuid
from app import db


class Wallet(db.Model):
    __tablename__ = 'wallets'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    owned_by = db.Column(db.String(36), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    enabled_at = db.Column(db.DateTime, nullable=False)
    balance = db.Column(db.Float, nullable=False, default=0)

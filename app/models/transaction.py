import uuid
from app import db


class Transaction(db.Model):
    """
        Transaction Model
    """
    __tablename__ = 'transactions'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    user_id = db.Column(db.String(36), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    transacted_at = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    reference_id = db.Column(db.String(36), unique=True, nullable=False)

    def __init__(self, user_id, status, transacted_at, type, amount, reference_id):
        self.user_id = user_id
        self.status = status
        self.transacted_at = transacted_at
        self.type = type
        self.amount = amount
        self.reference_id = reference_id

from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey, Integer, String, Column, Text, Enum
from datetime import datetime
from blueprints.user.model import Users
import enum

class Transaction(db.Model):
    __tablename__ = "transaction"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trx_code = db.Column(db.String(255), unique=True, nullable=False)
    payment_status = db.Column(db.Enum('lunas', 'belum lunas'), default='belum lunas')
    total_amount = db.Column(db.Numeric(12,2), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey(Users.id, ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    transaction_detail = db.relationship("TransactionDetail", cascade="all, delete-orphan", passive_deletes=True)
    shipping = db.relationship("Shipping", cascade="all, delete-orphan", passive_deletes=True)


    response_fields = {
        'id' : fields.Integer,
        'trx_code' : fields.String,
        'payment_status' :fields.String,
        'total_amount' : fields.Integer,
        'user_id' :fields.Integer,
        'created_at' : fields.String,
        'updated_at' : fields.String
    }

    def __init__(self, trx_code, payment_status, total_amount, user_id):
        self.trx_code = trx_code
        self.payment_status = payment_status
        self.total_amount = total_amount
        self.user_id = user_id
    def __repr__(self):
        return '<Transaction %r>' % self.id
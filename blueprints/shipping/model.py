from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func, expression
from sqlalchemy import ForeignKey, Integer, String, Column, Text
from datetime import datetime
from blueprints.transaction.model import Transaction

class Shipping(db.Model):
    __tablename__ = "shipping"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    transaction_id = db.Column(db.Integer, ForeignKey(Transaction.id, ondelete='CASCADE'), nullable=False)
    origin = db.Column(db.Integer, nullable=False)
    destination = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    fee = db.Column(db.Numeric(12,2), nullable=False)
    shipping_number = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    response_fields = {
        'id' : fields.Integer,
        'transaction_id' : fields.Integer,
        'origin' : fields.String,
        'destination' :fields.String,
        'weight' :fields.Integer,
        'fee' : fields.Integer,
        'shipping_number' : fields.String,
        'created_at' : fields.String,
        'updated_at' : fields.String
    }

    def __init__(self, transaction_id, origin, destination, weight, fee, shipping_number):
        self.transaction_id = transaction_id
        self.origin = origin
        self.destination = destination
        self.weight = weight
        self.fee = fee
        self.shipping_number = shipping_number
        
    def __repr__(self):
        return '<Shipping %r>' % self.id
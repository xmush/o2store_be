from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey, Integer, String, Column, Text
from datetime import datetime
from blueprints.transaction.model import Transaction
from blueprints.product.model import Product
from blueprints.user.model import Users

class TransactionDetail(db.Model):
	__tablename__ = "transaction_detail"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	note = db.Column(db.Text, nullable=True)
	qty = db.Column(db.Integer, nullable=False)
	transaction_id = db.Column(db.Integer, ForeignKey(Transaction.id, ondelete='CASCADE'), nullable=False)
	product_id = db.Column(db.Integer, ForeignKey(Product.id, ondelete='CASCADE'), nullable=False)
	user_id = db.Column(db.Integer, ForeignKey(Users.id, ondelete='CASCADE'), nullable=False)
	created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
	updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

	response_fields = {
		'id' : fields.Integer,
		'note' : fields.String,
		'qty' : fields.Integer,
		'transaction_id' : fields.Integer,
		'product_id' : fields.Integer,
		'user_id' : fields.Integer,
		'created_at' : fields.String,
		'updated_at' : fields.String
	}

	def __init__(self, note, qty, transaction_id, user_id, product_id):
		self.note = note
		self.qty = qty
		self.transaction_id = transaction_id
		self.user_id = user_id
		self.product_id = product_id
	def __repr__(self):
		return '<TransactionDetail %r>' % self.id
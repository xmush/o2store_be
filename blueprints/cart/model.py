from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey, Integer, String, Column, Text
from datetime import datetime
from blueprints.user.model import Users
from blueprints.product.model import Product

class Cart(db.Model):
	__tablename__ = "cart"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	note = db.Column(db.Text, nullable=True)
	qty = db.Column(db.Integer, nullable=False)
	user_id = db.Column(db.Integer, ForeignKey(Users.id, ondelete='CASCADE'), nullable=False)
	product_id = db.Column(db.Integer, ForeignKey(Product.id, ondelete='CASCADE'), nullable=False)
	created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
	updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

	response_fields = {
		'id' : fields.Integer,
		'note' : fields.String,
		'qty' : fields.Integer,
		'user_id' : fields.Integer,
		'product_id' : fields.Integer,
		'created_at' : fields.String,
		'updated_at' : fields.String
	}

	def __init__(self, note, qty, user_id, product_id):
		self.note = note
		self.qty = qty
		self.user_id = user_id
		self.product_id = product_id
	def __repr__(self):
		return '<Cart %r>' % self.id
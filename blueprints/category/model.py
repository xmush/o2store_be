from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey, Integer, String, Column, Text
from datetime import datetime

class Category(db.Model):
	__tablename__ = "category"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(100), nullable=False)
	description = db.Column(db.Text, nullable=False)
	created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
	updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
	product = db.relationship("Product", cascade="all, delete-orphan", passive_deletes=True)


	response_fields = {
		'id' : fields.Integer,
		'name' : fields.String,
		'description' : fields.String,
		'created_at' : fields.String,
		'updated_at' : fields.String
	}

	def __init__(self, name, description):
		self.name = name
		self.description = description

	def __repr__(self):
		return '<Category %r>' % self.id
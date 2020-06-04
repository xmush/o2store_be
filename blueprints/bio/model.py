from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey, Integer, String, Column, Text
from datetime import datetime

from blueprints.user.model import Users

class Bios(db.Model):
	__tablename__ = "bio"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	fullname = db.Column(db.String(100), nullable=False)
	address = db.Column(db.Text, nullable=False)
	contact = db.Column(db.String(15), nullable=False)
	sex = db.Column(db.String(1), nullable=True)
	user_id = db.Column(db.Integer, ForeignKey(Users.id, ondelete='CASCADE'), unique=True, nullable=False)
	created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
	updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

	response_fields = {
		'id' : fields.Integer,
		'fullname' : fields.String,
		'address' : fields.String,
		'contact' : fields.String,
		'sex' : fields.String,
		'user_id' : fields.Integer,
		'created_at' : fields.String,
		'updated_at' : fields.String
	}

	def __init__(self, fullname, address, contact, sex, user_id):
		self.fullname = fullname
		self.address = address
		self.contact = contact
		self.sex = sex
		self.user_id = user_id

	def __repr__(self):
		return '<Bio %r>' % self.id
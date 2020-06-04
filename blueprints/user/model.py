from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey, Integer, String, Column
from datetime import datetime

# from blueprints.client.model import Clients

class Users(db.Model):
	__tablename__ = "user"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(50), unique=True, nullable=False)
	email = db.Column(db.String(50), unique=True, nullable=False)
	password = db.Column(db.String(255), nullable=False)
	salt = db.Column(db.String(255), nullable=False)
	profil_img_path = db.Column(db.String(255), default='/storage/uploads/profil/user_default.png')
	role = db.Column(db.String(50), default='user')
	status = db.Column(db.Boolean, nullable=False, default=False)
	created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
	updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
	bio = db.relationship("Bios", cascade="all, delete-orphan", passive_deletes=True)
	product = db.relationship("Product", cascade="all, delete-orphan", passive_deletes=True)
	product_comment = db.relationship("ProductComment", cascade="all, delete-orphan", passive_deletes=True)
	product_like = db.relationship("ProductLike", cascade="all, delete-orphan", passive_deletes=True)
	cart = db.relationship("Cart", cascade="all, delete-orphan", passive_deletes=True)
	transaction = db.relationship("Transaction", cascade="all, delete-orphan", passive_deletes=True)
	transaction_detail = db.relationship("TransactionDetail", cascade="all, delete-orphan", passive_deletes=True)
	
	

    # to show respon field
	response_fields = {
		'id': fields.Integer,
		'username' : fields.String,
		'email': fields.String,
		'profil_img_path': fields.String,
		'role': fields.String,
		'status' : fields.Integer,
		'created_at' : fields.String,
		'updated_at' : fields.String
	}

	# to jwt claim response
	jwt_claim_fields = {
		'id' : fields.Integer,
		'role' : fields.String
	}

	def __init__(self, username, email, password, salt, profil_img_path, role):
		self.username = username
		self.email = email
		self.password = password
		self.salt = salt
		self.profil_img_path = profil_img_path
		self.role = role

	def __repr__(self):
		return '<User %r>' % self.id
from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey, Integer, String, Column, Text, Numeric
from datetime import datetime
from blueprints.category.model import Category
from blueprints.user.model import Users

class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric(12,2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, ForeignKey(Category.id, ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey(Users.id, ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    product_img = db.relationship("ProductImg", cascade="all, delete-orphan", passive_deletes=True)
    product_comment = db.relationship("ProductComment", cascade="all, delete-orphan", passive_deletes=True)
    product_like = db.relationship("ProductLike", cascade="all, delete-orphan", passive_deletes=True)
    cart = db.relationship("Cart", cascade="all, delete-orphan", passive_deletes=True)
    transaction_detail = db.relationship("TransactionDetail", cascade="all, delete-orphan", passive_deletes=True)


    response_fields = {
        'id' : fields.Integer,
        'name' : fields.String,
        'description' : fields.String,
        'price' : fields.Integer,
        'stock' : fields.Integer,
        'category_id' : fields.Integer,
        'user_id' : fields.Integer,
        'created_at' : fields.String,
        'updated_at' : fields.String
    }

    def __init__(self, name, description, price, stock, category_id, user_id):
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.category_id = category_id
        self.user_id = user_id

    def __repr__(self):
        return '<Product %r>' % self.id
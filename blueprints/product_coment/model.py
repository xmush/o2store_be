from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey, Integer, String, Column, Text, Numeric
from datetime import datetime
from blueprints.product.model import Product
from blueprints.user.model import Users

class ProductComment(db.Model):
    __tablename__ = "product_coment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    parent_id = db.Column(db.Integer, nullable=True, default=0)
    comment = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey(Users.id, ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, ForeignKey(Product.id, ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    response_fields = {
        'id' : fields.Integer,
        'parent_id' : fields.Integer,
        'comment' : fields.String,
        'user_id' : fields.Integer,
        'product_id' : fields.Integer,
        'created_at' : fields.String,
        'updated_at' : fields.String
    }

    def __init__(self, parent_id, comment, user_id, product_id):
        self.parent_id = parent_id
        self.comment = comment
        self.user_id = user_id
        self.product_id = product_id

    def __repr__(self):
        return '<ProductComment %r>' % self.id
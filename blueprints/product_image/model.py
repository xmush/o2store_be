from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey, Integer, String, Column, Text, Numeric
from datetime import datetime
from blueprints.product.model import Product

class ProductImg(db.Model):
    __tablename__ = "product_img"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    img_path = db.Column(db.Text, nullable=False)
    img_desc = db.Column(db.Text, nullable=False)
    product_id = db.Column(db.Integer, ForeignKey(Product.id, ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    response_fields = {
        'id' : fields.Integer,
        'img_path' : fields.String,
        'img_desc' : fields.String,
        'product_id' : fields.Integer,
        'created_at' : fields.String,
        'updated_at' : fields.String
    }

    def __init__(self, img_path, img_desc, product_id):
        self.img_path = img_path
        self.img_desc = img_desc
        self.product_id = product_id

    def __repr__(self):
        return '<ProductImg %r>' % self.id
from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal
from sqlalchemy import desc
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints import db, app, admin_required
import werkzeug, os, requests, json
# from blueprints.user.model import Users

import hashlib, uuid


from blueprints.product.model import Product
from blueprints.product_image.model import ProductImg
from blueprints.helper import sendImageToImgur
bp_user_product = Blueprint('user_product', __name__)
api = Api(bp_user_product)

class UserProductResource(Resource) :
    def __init__(self) :
        pass
    
    # @jwt_required
    # def get(self, id) : 
    #     qry = Product.query.get(id) 
    #     if qry is not None :
    #         return marshal(qry, Product.response_fields), 200
    #     return {'status': 'NOT_FOUND'}, 404
    
    # @internal_required    
    @jwt_required
    def post(self) :
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='form', required=True)
        parser.add_argument('description', location='form', required=True)
        parser.add_argument('category_id', location='form', type=int, required=True)
        parser.add_argument('price', location='form', type=int, required=True)
        parser.add_argument('stock', location='form', type=int, required=True)
        parser.add_argument('img_product', type=werkzeug.datastructures.FileStorage, location='files', required=True)
        parser.add_argument('img_description', location='form')
        args=parser.parse_args()

        # get user id from jwt claim
        claim = get_jwt_claims()
        user_id = claim['id']

        imageUrl = sendImageToImgur(args['img_product'])

        product = Product(args['name'], args['description'], args['price'], args['stock'], args['category_id'], user_id)
        db.session.add(product)
        db.session.flush()

        product_img = ProductImg(imageUrl, args['img_description'], product.id)
        db.session.add(product_img)

        db.session.commit()

        app.logger.debug('DEBUG : %s', product)
        app.logger.debug('DEBUG : %s', product_img)

        return [marshal(product, Product.response_fields), marshal(product_img, ProductImg.response_fields)], 200
    # @jwt_required
    # def put(self, id) :

    #     qry = Product.query.get(id)
        
    #     parser = reqparse.RequestParser()
    #     parser.add_argument('name', location='json', default=qry.name)
    #     parser.add_argument('description', location='json', default=qry.description)
    #     parser.add_argument('price', location='json', type=int, default=qry.price)
    #     parser.add_argument('stock', location='json', type=int, default=qry.stock)
    #     parser.add_argument('category_id', location='json', default=qry.category_id)
    #     args=parser.parse_args()

    #     if qry is None :
    #         return {'status' : 'NOT_FOUND'}, 404

    #     claim = get_jwt_claims()
    #     user_id = claim['id']

    #     qry.name = args['name']
    #     qry.description = args['description']
    #     qry.price = args['price']
    #     qry.stock = args['stock']
    #     qry.category_id = args['category_id']
    #     qry.user_id = user_id

    #     db.session.commit()

    #     app.logger.debug('DEBUG : %s', qry)

    #     return marshal(qry, Product.response_fields), 200, {'Content-Type': 'application/json'}

    # @jwt_required
    # def delete(self, id) :
    #     claim = get_jwt_claims()
    #     user_id = claim['id']
    #     qry = Product.query.get(id)
    #     if qry is None :
    #         return {'status' : 'NOT_FOUND'}, 404
    #     elif qry.user_id != user_id :
    #         return {'status' : 'Method_Not_Allowed'}, 405
    #     db.session.delete(qry)
    #     db.session.commit()

    #     return {'status': 'DELETED'}, 200


class UserProductList(Resource):

    def __init__(self):
        pass
    # @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('order_by', type=int, location='args', help='invalid orderby value', choices=('id','name', 'price', 'stock', 'category_id', 'user_id'), default='id')
        parser.add_argument('sort', location='args', help='invalid sort value', choices=('desc', 'asc'), default='desc')
        args = parser.parse_args()

        if args['p'] == 1 :
            offset = 0
        else :
            offset = args['p'] * args['rp'] - args['rp']
        
        qry = Product.query

        if args['order_by'] == 'id' :
            if args['sort'] == 'desc' :
                qry = qry.order_by(desc(Product.id))
            else :
                qry = qry.order_by(Product.id)
        if args['order_by'] == 'name' :
            if args['sort'] == 'desc' :
                qry = qry.order_by(desc(Product.name))
            else :
                qry = qry.order_by(Product.name)
        elif args['order_by'] == 'price' :
            if args['sort'] == 'desc' :
                qry = qry.order_by(desc(Product.price))
            else :
                qry = qry.order_by(Product.price)
        elif args['order_by'] == 'stock' :
            if args['sort'] == 'desc' :
                qry = qry.order_by(desc(Product.stock))
            else :
                qry = qry.order_by(Product.stock)            
        elif args['order_by'] == 'category_id' :
            if args['sort'] == 'desc' :
                qry = qry.order_by(desc(Product.category_id))
            else :
                qry = qry.order_by(Product.category_id)            
        elif args['order_by'] == 'user_id' :
            if args['sort'] == 'desc' :
                qry = qry.order_by(desc(Product.user_id))
            else :
                qry = qry.order_by(Product.user_id)

        rows = []
        i = 0
        for row in qry.limit(args['rp']).offset(offset).all() :
            img = ProductImg.query.filter_by(product_id=row.id).first()
            dataImg = marshal(img, ProductImg.response_fields)
            rows.append(marshal(row, Product.response_fields)) 
            rows[i]["image"]=dataImg
            i += 1
        return rows, 200

class UserProductByCategory(Resource) :
    def __init__(self) :
        pass

    def get(self, id) :
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('order_by', type=int, location='args', help='invalid orderby value', choices=('id','name', 'price', 'stock', 'category_id', 'user_id'), default='id')
        parser.add_argument('sort', location='args', help='invalid sort value', choices=('desc', 'asc'), default='desc')
        args = parser.parse_args()

        if args['p'] == 1 :
            offset = 0
        else :
            offset = args['p'] * args['rp'] - args['rp']
        
        qry = Product.query.filter_by(category_id=id)

        if args['order_by'] == 'id' :
            if args['sort'] == 'desc' :
                qry = qry.order_by(desc(Product.id))
            else :
                qry = qry.order_by(Product.id)
        if args['order_by'] == 'name' :
            if args['sort'] == 'desc' :
                qry = qry.order_by(desc(Product.name))
            else :
                qry = qry.order_by(Product.name)
        elif args['order_by'] == 'price' :
            if args['sort'] == 'desc' :
                qry = qry.order_by(desc(Product.price))
            else :
                qry = qry.order_by(Product.price)
        elif args['order_by'] == 'stock' :
            if args['sort'] == 'desc' :
                qry = qry.order_by(desc(Product.stock))
            else :
                qry = qry.order_by(Product.stock)            
        elif args['order_by'] == 'category_id' :
            if args['sort'] == 'desc' :
                qry = qry.order_by(desc(Product.category_id))
            else :
                qry = qry.order_by(Product.category_id)            
        elif args['order_by'] == 'user_id' :
            if args['sort'] == 'desc' :
                qry = qry.order_by(desc(Product.user_id))
            else :
                qry = qry.order_by(Product.user_id)

        rows = []
        i = 0
        for row in qry.limit(args['rp']).offset(offset).all() :
            img = ProductImg.query.filter_by(product_id=row.id).first()
            dataImg = marshal(img, ProductImg.response_fields)
            rows.append(marshal(row, Product.response_fields)) 
            rows[i]["image"]=dataImg
            i += 1
        return rows, 200        


api.add_resource(UserProductByCategory, '', '/category/<id>')
api.add_resource(UserProductList, '', '/list')
api.add_resource(UserProductResource, '', '/<id>')

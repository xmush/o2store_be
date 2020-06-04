from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal
from sqlalchemy import desc
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints import db, app, admin_required
# from blueprints.user.model import Users

import hashlib, uuid


from .model import Transaction
bp_transaction = Blueprint('transaction', __name__)
api = Api(bp_transaction)

class TransactionResource(Resource) :
    def __init__(self) :
        pass
    
    # @jwt_required
    # def get(self, id) : 
    #     qry = Product.query.get(id) 
    #     if qry is not None :
    #         return marshal(qry, Product.response_fields), 200
    #     return {'status': 'NOT_FOUND'}, 404
    
    # # @internal_required    
    # @jwt_required
    # def post(self) :
    #     parser = reqparse.RequestParser()
    #     parser.add_argument('name', location='json', required=True)
    #     parser.add_argument('description', location='json', required=True)
    #     parser.add_argument('price', location='json', type=int, required=True)
    #     parser.add_argument('stock', location='json', type=int, required=True)
    #     parser.add_argument('category_id', location='json', required=True)
    #     # parser.add_argument('description', location='json', required=True)
    #     args=parser.parse_args()

    #     # get user id from jwt claim
    #     claim = get_jwt_claims()
    #     user_id = claim['id']

    #     product = Product(args['name'], args['description'], args['price'], args['stock'], args['category_id'], user_id)

    #     db.session.add(product)
    #     db.session.commit()

    #     app.logger.debug('DEBUG : %s', product)

    #     return marshal(product, Product.response_fields), 200, {'Content-Type': 'application/json'}

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


class TransactionList(Resource):

    def __init__(self):
        pass
    # @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('order_by', type=int, location='args', help='invalid orderby value', choices=('created_at', 'id', 'user_id', 'payment_status', 'total_amount'))
        parser.add_argument('sort', location='args', help='invalid sort value', choices=('desc', 'asc'))
        args = parser.parse_args()

        if args['p'] == 1 :
            offset = 0
        else :
            offset = args['p'] * args['rp'] - args['rp']
        
        qry = Transaction.query

        if args['order_by'] == 'created_at' :
            if args['sort'] == 'desc' :
                qry = qry.order_by(desc(Transaction.created_at))
            else :
                qry = qry.order_by(Transaction.created_at)
        elif args['order_by'] == 'id' :
            if args['sort'] == 'desc' :
                qry = qry.order_by(desc(Transaction.id))
            else :
                qry = qry.order_by(Transaction.id)
        elif args['order_by'] == 'user_id' :
            if args['sort'] == 'desc' :
                qry = qry.order_by(desc(Transaction.user_id))
            else :
                qry = qry.order_by(Transaction.user_id)            
        elif args['order_by'] == 'total_amount' :
            if args['sort'] == 'desc' :
                qry = qry.order_by(desc(Transaction.total_amount))
            else :
                qry = qry.order_by(Transaction.total_amount)            
        elif args['order_by'] == 'payment_status' :
            if args['sort'] == 'desc' :
                qry = qry.order_by(desc(Transaction.payment_status))
            else :
                qry = qry.order_by(Transaction.payment_status)

        rows = []

        for row in qry.limit(args['rp']).offset(offset).all() :
            rows.append(marshal(row, Transaction.response_fields)) 
        return rows, 200

api.add_resource(TransactionList, '', '/list')
api.add_resource(TransactionResource, '', '/<id>')
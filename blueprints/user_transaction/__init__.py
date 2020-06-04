from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal
from sqlalchemy import desc
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints import db, app, admin_required
import werkzeug, os, requests, json
# from blueprints.user.model import Users

import hashlib, uuid


from blueprints.cart.model import Cart
from blueprints.transaction.model import Transaction
from blueprints.transaction_detail.model import TransactionDetail
from blueprints.product.model import Product
bp_user_transaction = Blueprint('user_transaction', __name__)
api = Api(bp_user_transaction)

class UserTransactionResource(Resource) :
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
        parser.add_argument('do_trasaction', location='json', required=True)
        args=parser.parse_args()
        
        claim = get_jwt_claims()
        user_id = claim['id']
        
        userCart = Cart.query.filter_by(user_id=user_id).all()
        # print(userCart.length)
        if len(userCart) == 0 :
            return {'msg' : 'data not found'}, 404

        # insert into transaction
        trx_code = uuid.uuid4().hex
        total_amount = 0
        trx_dtl = []
        for cartItem in userCart :
            product = Product.query.get(cartItem.product_id)
            price = product.price * cartItem.qty
            total_amount += price
            trx_dtl.append([cartItem.note, cartItem.qty, user_id, cartItem.product_id])
            db.session.delete(Cart.query.get(cartItem.id))

        trx = Transaction(trx_code, 'belum lunas', total_amount, user_id)
        db.session.add(trx)
        db.session.flush()

        trd_log = []
        trd_marsal = []
        for dtl in trx_dtl :
            trd = TransactionDetail(dtl[0], dtl[1], trx.id, dtl[2], dtl[3])
            db.session.add(trd)
            trd_log.append(trd)
            trd_marsal.append(marshal(trd, TransactionDetail.response_fields))
            # db.session.remove(Cart.query.get())
        
        db.session.commit()
        
        app.logger.debug('DEBUG : %s', trx)
        app.logger.debug('DEBUG : %s', trd_log)

        trx_response = marshal(trx, Product.response_fields)
        trx_response['detail'] = trd_marsal

        return trx_response, 200



        # for i in range(len(newData)) :
            # print(i)
        # print('============================\n')
        
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


class UserTransactionList(Resource):

    def __init__(self):
        pass
    @jwt_required
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
        
        
        claim = get_jwt_claims()
        user_id = claim['id']


        qry = Transaction.query.filter_by(user_id=user_id)

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
        i = 0
        for row in qry.limit(args['rp']).offset(offset).all() :
            td = []
            trx_dtl = TransactionDetail.query.filter_by(transaction_id=row.id).all()
            x=0
            for item in trx_dtl :
                produk = Product.query.get(item.product_id)
                td.append(marshal(item, TransactionDetail.response_fields))
                td[x]['produk'] = marshal(produk, Product.response_fields)
                x+=1
            rows.append(marshal(row, Transaction.response_fields))
            rows[i]['detail'] = td
            i+=1

        return rows, 200

api.add_resource(UserTransactionList, '', '/list')
api.add_resource(UserTransactionResource, '', '/<id>')

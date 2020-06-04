from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal
from sqlalchemy import desc
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints import db, app, admin_required
# from blueprints.user.model import Users

import hashlib, uuid


from .model import TransactionDetail
bp_transaction_detail = Blueprint('transaction_detail', __name__)
api = Api(bp_transaction_detail)

class TransactionDetailResource(Resource) :
    def __init__(self) :
        pass
    
    # @jwt_required
    # def get(self, id) : 
    #     qry = TransactionDetail.query.get(id) 
    #     if qry is not None :
    #         return marshal(qry, TransactionDetail.response_fields), 200
    #     return {'status': 'NOT_FOUND'}, 404
    
    # # @internal_required    
    # @jwt_required
    # def post(self) :
    #     parser = reqparse.RequestParser()
    #     parser.add_argument('note', location='json', required=False)
    #     parser.add_argument('trx_dtl', location='json', required=True)
    #     parser.add_argument('qty', location='json', type=int, default=1, required=True)
    #     parser.add_argument('product_id', location='json', type=int, required=True)
    #     args=parser.parse_args()

    #     # get user id from jwt claim
    #     claim = get_jwt_claims()
    #     user_id = claim['id']

    #     data_trx_dtl = TransactionDetail.query.filter_by(product_id=args['product_id']).first()
    #     if data_trx_dtl is not None :
    #         update_trx_dtl = TransactionDetail.query.get(data_trx_dtl.id)
    #         update_trx_dtl.qty = update_trx_dtl.qty + args['qty']
    #         db.session.commit()
    #         app.logger.debug('DEBUG : %s', update_trx_dtl)
    #         return marshal(update_trx_dtl, TransactionDetail.response_fields), 200, {'Content-Type': 'application/json'}


    #     trx_dtl = TransactionDetailList(args['note'], args['trx_dtl'], args['qty'], user_id, args['product_id'])

    #     db.session.add(trx_dtl)
    #     db.session.commit()

    #     app.logger.debug('DEBUG : %s', trx_dtl)

    #     return marshal(trx_dtl, TransactionDetailList.response_fields), 200, {'Content-Type': 'application/json'}

    # @jwt_required
    # def put(self, id) :

    #     qry = TransactionDetail.query.get(id)
    #     parser = reqparse.RequestParser()
    #     parser.add_argument('note', location='json', required=False)
    #     parser.add_argument('qty', location='json', type=int, default=1, required=True)
    #     parser.add_argument('product_id', location='json', type=int, required=True)
    #     args=parser.parse_args()

    #     if qry is None :
    #         return {'status' : 'NOT_FOUND'}, 404

    #     claim = get_jwt_claims()
    #     user_id = claim['id']

    #     if qry.user_id != user_id :
    #         return {'status' : 'Method_Not_Allowed'}, 405

    #     if args['note'] is not None :
    #         qry.note = args['note']
    #     if args['qty'] is not None :
    #         qry.qty = args['qty']
    #     if args['product_id'] is not None :
    #         qry.product_id = args['product_id']

    #     # qry.user_id = user_id

    #     db.session.commit()

    #     app.logger.debug('DEBUG : %s', qry)

    #     return marshal(qry, TransactionDetail.response_fields), 200, {'Content-Type': 'application/json'}

    # @jwt_required
    # def delete(self, id) :
    #     claim = get_jwt_claims()
    #     user_id = claim['id']
    #     qry = TransactionDetail.query.get(id)
    #     if qry is None :
    #         return {'status' : 'NOT_FOUND'}, 404
    #     elif qry.user_id != user_id :
    #         return {'status' : 'Method_Not_Allowed'}, 405
    #     db.session.delete(qry)
    #     db.session.commit()

    #     return {'status': 'DELETED'}, 200


class TransactionDetailList(Resource):

    def __init__(self):
        pass
    # # @internal_required
    # def get(self):
    #     parser = reqparse.RequestParser()
    #     parser.add_argument('p', type=int, location='args', default=1)
    #     parser.add_argument('rp', type=int, location='args', default=25)
    #     parser.add_argument('order_by', type=int, location='args', help='invalid orderby value', choices=('user_id', 'produck_id'))
    #     parser.add_argument('sort', location='args', help='invalid sort value', choices=('desc', 'asc'))
    #     args = parser.parse_args()

    #     if args['p'] == 1 :
    #         offset = 0
    #     else :
    #         offset = args['p'] * args['rp'] - args['rp']
        
    #     qry = TransactionDetail.query

    #     if args['order_by'] == 'user_id' :
    #         if args['sort'] == 'desc' :
    #             qry = qry.order_by(desc(TransactionDetail.user_id))
    #         else :
    #             qry = qry.order_by(TransactionDetail.user_id)
    #     elif args['order_by'] == 'produck_id' :
    #         if args['sort'] == 'desc' :
    #             qry = qry.order_by(desc(TransactionDetail.produck_id))
    #         else :
    #             qry = qry.order_by(TransactionDetail.produck_id)

    #     rows = []

    #     for row in qry.limit(args['rp']).offset(offset).all() :
    #         rows.append(marshal(row, TransactionDetail.response_fields)) 
    #     return rows, 200

api.add_resource(TransactionDetailList, '', '/list')
api.add_resource(TransactionDetailResource, '', '/<id>')

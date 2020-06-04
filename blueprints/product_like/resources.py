from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal
from sqlalchemy import desc
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints import db, app, admin_required
# from blueprints.user.model import Users

import hashlib, uuid


from .model import ProductLike
bp_product_like = Blueprint('product_like', __name__)
api = Api(bp_product_like)

class ProductLikeResource(Resource) :
    def __init__(self) :
        pass
    
    # @jwt_required
    def get(self, id) : 
        qry = ProductLike.query.get(id) 
        if qry is not None :
            return marshal(qry, ProductLike.response_fields), 200
        return {'status': 'NOT_FOUND'}, 404
    
    # @internal_required    
    @jwt_required
    def post(self) :
        parser = reqparse.RequestParser()
        parser.add_argument('product_id', location='json', type=int, required=True)
        args=parser.parse_args()

        # get user id from jwt claim
        claim = get_jwt_claims()
        user_id = claim['id']

        like = ProductLike.query.filter_by(user_id = user_id).first()
        
        if like is not None :

            qry = ProductLike.query.get(like.id)

            db.session.delete(qry)
            db.session.commit()

            return {'status': 'DELETED'}, 200

        like = ProductLike(user_id, args['product_id'])

        db.session.add(like)
        db.session.commit()

        app.logger.debug('DEBUG : %s', like)

        return marshal(like, ProductLike.response_fields), 200, {'Content-Type': 'application/json'}

    @jwt_required
    def put(self, id) :

        qry = ProductLike.query.get(id)
        
        parser = reqparse.RequestParser()
        parser.add_argument('product_id', location='json', type=int, required=True)
        args=parser.parse_args()

        if qry is None :
            return {'status' : 'NOT_FOUND'}, 404

        claim = get_jwt_claims()
        user_id = claim['id']

        if qry.user_id != user_id :
            return {'status' : 'Method_Not_Allowed'}, 405

        if args['product_id'] is not None :
            qry.product_id = args['product_id']

        # qry.user_id = user_id

        db.session.commit()

        app.logger.debug('DEBUG : %s', qry)

        return marshal(qry, ProductLike.response_fields), 200, {'Content-Type': 'application/json'}

    @jwt_required
    def delete(self, id) :
        claim = get_jwt_claims()
        user_id = claim['id']
        qry = ProductLike.query.get(id)
        if qry is None :
            return {'status' : 'NOT_FOUND'}, 404
        elif qry.user_id != user_id :
            return {'status' : 'Method_Not_Allowed'}, 405
        db.session.delete(qry)
        db.session.commit()

        return {'status': 'DELETED'}, 200


class ProductLiketList(Resource):

    def __init__(self):
        pass
    # @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('order_by', type=int, location='args', help='invalid orderby value', choices=('user_id', 'produck_id'))
        parser.add_argument('sort', location='args', help='invalid sort value', choices=('desc', 'asc'))
        args = parser.parse_args()

        if args['p'] == 1 :
            offset = 0
        else :
            offset = args['p'] * args['rp'] - args['rp']
        
        qry = ProductLike.query


        if args['order_by'] == 'user_id' :
            if args['sort'] == 'desc' :
                qry = qry.order_by(desc(ProductLike.user_id))
            else :
                qry = qry.order_by(ProductLike.user_id)
        elif args['order_by'] == 'produck_id' :
            if args['sort'] == 'desc' :
                qry = qry.order_by(desc(ProductLike.produck_id))
            else :
                qry = qry.order_by(ProductLike.produck_id)

        rows = []

        for row in qry.limit(args['rp']).offset(offset).all() :
            rows.append(marshal(row, ProductLike.response_fields)) 
        return rows, 200

api.add_resource(ProductLiketList, '', '/list')
api.add_resource(ProductLikeResource, '', '/<id>')

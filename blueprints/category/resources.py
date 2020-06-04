from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal
from sqlalchemy import desc
from flask_jwt_extended import jwt_required
from blueprints import db, app, admin_required
# from blueprints.user.model import Users

import hashlib, uuid


from .model import Category
bp_category = Blueprint('category', __name__)
api = Api(bp_category)

class BioResource(Resource) :
    def __init__(self) :
        pass
    
    # @jwt_required
    def get(self, id) : 
        qry = Category.query.get(id) 
        if qry is not None :
            return marshal(qry, Category.response_fields), 200
        return {'status': 'NOT_FOUND'}, 404
    
    # @internal_required    
    # @jwt_required
    def post(self) :
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('description', location='json', required=True)
        args=parser.parse_args()
        
        cat = Category(args['name'], args['description'])

        db.session.add(cat)
        db.session.commit()

        app.logger.debug('DEBUG : %s', cat)

        return marshal(cat, Category.response_fields), 200, {'Content-Type': 'application/json'}

    # @jwt_required
    def put(self, id) :
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('description', location='json', required=True)
        args=parser.parse_args()

        qry = Category.query.get(id)
        if qry is None :
            return {'status' : 'NOT_FOUND'}, 404

        qry.name = args['name']
        qry.description = args['description']

        db.session.commit()

        app.logger.debug('DEBUG : %s', qry)

        return marshal(qry, Category.response_fields), 200, {'Content-Type': 'application/json'}

    # @internal_required
    def delete(self, id) :
        qry = Category.query.get(id)
        if qry is None :
            return {'status' : 'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()

        return {'status': 'DELETED'}, 200


class BioList(Resource):

    def __init__(self):
        pass
    
    # @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('sort', location='args', help='invalid sort value', choices=('desc', 'asc'))
        args = parser.parse_args()

        if args['p'] == 1 :
            offset = 0
        else :
            offset = args['p'] * args['rp'] - args['rp']
        
        qry = Category.query

        if args['sort'] == 'desc' :
            qry = qry.order_by(desc(Category.id))
        else :
            qry = qry.order_by(Category.id)

        rows = []

        for row in qry.limit(args['rp']).offset(offset).all() :
            rows.append(marshal(row, Category.response_fields)) 
        return rows, 200

api.add_resource(BioList, '', '/list')
api.add_resource(BioResource, '', '/<id>')

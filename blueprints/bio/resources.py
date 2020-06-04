from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal
from sqlalchemy import desc
from flask_jwt_extended import jwt_required
from blueprints import db, app, admin_required
from blueprints.user.model import Users

import hashlib, uuid


from .model import Bios
bp_bio = Blueprint('bio', __name__)
api = Api(bp_bio)

class BioResource(Resource) :
    def __init__(self) :
        pass
    
    # @jwt_required
    def get(self, id) : 
        qry = Users.query.get(id) 
        if qry is not None :
            return marshal(qry, Users.response_fields), 200
        return {'status': 'NOT_FOUND'}, 404
    
#     # @internal_required    
    # @jwt_required
    def post(self, id) :
        parser = reqparse.RequestParser()
        parser.add_argument('fullname', location='json', required=True)
        parser.add_argument('address', location='json', required=True)
        parser.add_argument('contact', location='json', required=True)
        parser.add_argument('sex', location='json', choices=('F', 'M'), required=True)
        args=parser.parse_args()

        checkIfExist = Bios.query.filter_by(user_id=id).first()

        if checkIfExist is not None :
            return {'status' : 'USER_ID_ALREADY_EXIST'}, 404

        
        bio = Bios(args['fullname'], args['address'], args['contact'], args['sex'], id)

        db.session.add(bio)
        db.session.commit()

        app.logger.debug('DEBUG : %s', bio)

        return marshal(bio, Bios.response_fields), 200, {'Content-Type': 'application/json'}

#     @jwt_required
    def put(self, id) :
        parser = reqparse.RequestParser()
        parser.add_argument('fullname', location='json', required=True)
        parser.add_argument('address', location='json', required=True)
        parser.add_argument('contact', location='json', required=True) 
        parser.add_argument('sex', location='json', choices=('F', 'M'), required=True)
        args=parser.parse_args()

        userQry = Users.query.get(id)
        if userQry is None :
            return {'status' : 'USER_NOT_FOUND'}, 404


        qry = Bios.query.filter_by(user_id=id).first()
        if qry is None :
            return {'status' : 'NOT_FOUND'}, 404

        qry.fullname = args['fullname']
        qry.address = args['address']
        qry.contact = args['contact']
        qry.sex = args['sex']

        db.session.commit()

        app.logger.debug('DEBUG : %s', qry)

        return marshal(qry, Bios.response_fields), 200, {'Content-Type': 'application/json'}

    # @internal_required
    def delete(self, id) :
        bio = Bios.query.filter_by(user_id=id).first()
        qry = Bios.query.get(bio.id)
        if qry is None :
            return {'status' : 'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()

        return {'status': 'DELETED'}, 200


class BioList(Resource):

    def __init__(self):
        pass
    # @internal_required
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
        
        qry = Bios.query

        if args['sort'] == 'desc' :
            qry = qry.order_by(desc(Bios.id))
        else :
            qry = qry.order_by(Bios.id)

        rows = []

        for row in qry.limit(args['rp']).offset(offset).all() :
            rows.append(marshal(row, Bios.response_fields)) 
        return rows, 200

api.add_resource(BioList, '', '/list')
api.add_resource(BioResource, '', '/<id>')

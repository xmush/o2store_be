from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal
from sqlalchemy import desc
from flask_jwt_extended import jwt_required
from blueprints import db, app, admin_required

import hashlib, uuid


from .model import Users
from blueprints.bio.model import Bios
bp_user = Blueprint('user', __name__)
api = Api(bp_user)

class UserResource(Resource) :
    def __init__(self) :
        pass
    
    # @admin_required
    def get(self, id) : 
        qry = Users.query.get(id)
        bio = Bios.query.filter_by(user_id = id).first()
        print("marhal response : ", marshal(qry, Users.response_fields))

        marged = marshal(qry, Users.response_fields)
        marged['biodata'] = marshal(bio, Bios.response_fields)

        print("marged response : ", marged)
        if qry is not None :
            return marged, 200
        return {'status': 'NOT_FOUND'}, 404
    
#     # @jwt_required
#     # @admin_required    
    def post(self) :
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        args=parser.parse_args()

        salt = uuid.uuid4().hex
        hs = ('%s%s' % (args['password'],salt)).encode('utf-8')
        clientsec = hashlib.sha512(hs).hexdigest()
        args['password'] = clientsec.encode('utf-8')

        # initiating profil img path
        img_path = None

        # initiating role
        role = 'user'

        user = Users(args['username'], args['email'], args['password'], salt, img_path, role)

        db.session.add(user)
        db.session.commit()

        app.logger.debug('DEBUG : %s', user)

        return marshal(user, Users.response_fields), 200, {'Content-Type': 'application/json'}

    # @jwt_required
    @admin_required
    def put(self, id) :
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('role', location='json', choices=('user', 'admin'), required=True)
        parser.add_argument('status', location='json', type=bool, required=True)
        args=parser.parse_args()

        qry = Users.query.get(id)


        if qry is None :
            return {'status' : 'NOT_FOUND'}, 404

        qry.username = args['username']
        qry.email = args['email']
        qry.role = args['role']
        qry.status = args['status']

        db.session.commit()

        app.logger.debug('DEBUG : %s', qry)

        return marshal(qry, Users.response_fields), 200, {'Content-Type': 'application/json'}

    @admin_required
    def delete(self, id) :
        qry = Users.query.get(id)
        if qry is None :
            return {'status' : 'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()

        return {'status': 'DELETED'}, 200


class UserList(Resource):

    def __init__(self):
        pass
    
    @admin_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('order_by', location='args', help='invalid orderby value', choices=('username', 'email', 'role', 'created_at'))
        parser.add_argument('sort', location='args', help='invalid sort value', choices=('desc', 'asc'))

        args = parser.parse_args()

        if args['p'] == 1 :
            offset = 0
        else :
            offset = args['p'] * args['rp'] - args['rp']
        
        qry = Users.query


        if args['order_by'] == 'username' : 
            if args['sort'] == 'desc' :
                qry = qry.order_by(desc(Users.username))
            else :
                qry = qry.order_by(Users.username)

        elif args['order_by'] == 'email' :
            if args['sort'] == 'desc' :
                qry = qry.order_by(desc(Users.email))
            else :
                qry = qry.order_by(Users.email)

        elif args['order_by'] == 'role' :
            if args['sort'] == 'desc' :
                qry = qry.order_by(desc(Users.role))
            else :
                qry = qry.order_by(Users.role)

        elif args['order_by'] == 'created_at' :
            if args['sort'] == 'desc' :
                qry = qry.order_by(desc(Users.role))
            else :
                qry = qry.order_by(Users.role)

        else :
            if args['sort'] == 'desc' :
                qry = qry.order_by(desc(Users.id))
            else :
                qry = qry.order_by(Users.id)

        rows = []

        for row in qry.limit(args['rp']).offset(offset).all() :
            rows.append(marshal(row, Users.response_fields)) 

        return rows, 200

    # def post(self) :
    #     return {'message': 'success', 'status' : '200 OK'}, 200

api.add_resource(UserList, '', '/list')
api.add_resource(UserResource, '', '/<id>')

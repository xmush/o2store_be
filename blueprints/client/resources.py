from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal
from sqlalchemy import desc
from flask_jwt_extended import jwt_required
# from app import db
from blueprints import db, app, admin_required

import hashlib, uuid

# from . import Clients, Client
from .model import Clients
bp_client = Blueprint('client', __name__)
api = Api(bp_client)

class ClientsResource(Resource) :
    # clients = Clients()
    def __init__(self) :
        pass
    
    @jwt_required
    # @interna
    def get(self, id) : 
        qry = Clients.query.get(id) 
        if qry is not None :
            return marshal(qry, Clients.response_fields), 200
        return {'status': 'NOT_FOUND'}, 404
    
    # @jwt_required
    # @admin_required    
    def post(self) :
        parser = reqparse.RequestParser()
        #get data from request json
        parser.add_argument('status', location='json', type=bool, required=True)
        parser.add_argument('client_secret', location='json', required=True)
        parser.add_argument('client_key', location='json', required=True)
        args=parser.parse_args()

        salt = uuid.uuid4().hex
        hs = ('%s%s' % (args['client_secret'],salt)).encode('utf-8')
        clientsec = hashlib.sha512(hs).hexdigest()
        # type(clientsec)
        args['client_secret'] = clientsec.encode('utf-8')

        # print(args['status'], args['client_secret'], args['client_key'], salt, args['client_secret'])
        client = Clients(args['status'], args['client_secret'], args['client_key'], salt, args['client_secret'])

        db.session.add(client)
        db.session.commit()

        app.logger.debug('DEBUG : %s', client)

        return marshal(client, Clients.response_fields), 200, {'Content-Type': 'application/json'}

    @jwt_required
    def put(self, id) :
        parser = reqparse.RequestParser()
        #get data from request json
        parser.add_argument('status', location='json', type=bool, required=True)
        parser.add_argument('client_secret', location='json', required=True)
        parser.add_argument('client_key', location='json', required=True)   
        args=parser.parse_args()

        # client = Clients(args['status'], args['client_secret'], args['client_key'], args['created_at'], args['updated_at'], args['deleted_at'])

        qry = Clients.query.get(id)


        if qry is None :
            return {'status' : 'NOT_FOUND'}, 404

        salt = qry.salt
        hs = ('%s%s' % (args['client_secret'],salt)).encode('utf-8')
        clientsec = hashlib.sha512(hs).hexdigest()
        # args['client_secret'] = clientsec.encode('utf-8')

        print(salt)

        qry.status = args['status']
        qry.client_secret = clientsec.encode('utf-8')
        qry.client_key = args['client_key']

        db.session.commit()

        # return marshal(qry, Clients.response_fields), 200

        app.logger.debug('DEBUG : %s', qry)

        return marshal(qry, Clients.response_fields), 200, {'Content-Type': 'application/json'}

    @admin_required
    def delete(self, id) :
        qry = Clients.query.get(id)
        if qry is None :
            return {'status' : 'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()

        return {'status': 'DELETED'}, 200


class ClientLists(Resource):

    def __init__(self):
        pass
    @admin_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('orderby', location='args', help='invalid orderby value', choices=('status'))
        parser.add_argument('sort', location='args', help='invalid sort value', choices=('desc', 'asc'))

        args = parser.parse_args()

        if args['p'] == 1 :
            offset = 0
        else :
            offset = args['p'] * args['rp'] - args['rp']
        
        qry = Clients.query

        if args['orderby'] is not None :
            if args['sort'] == 'desc' :
                qry = qry.order_by(desc(Clients.status))
            else :
                qry = qry.order_by(Clients.status)

        rows = []

        for row in qry.limit(args['rp']).offset(offset).all() :
            rows.append(marshal(row, Clients.response_fields)) 


        return rows, 200
api.add_resource(ClientLists, '', '/list')
api.add_resource(ClientsResource, '', '/<id>')

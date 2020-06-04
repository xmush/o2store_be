from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal
from sqlalchemy import desc
from flask_jwt_extended import jwt_required
from blueprints import db, app, admin_required
from blueprints.user.model import Users
from blueprints.bio.model import Bios

import hashlib, uuid

bp_register = Blueprint('register', __name__)
api = Api(bp_register)

class RegisterResource(Resource) :
    def __init__(self) :
        pass

    def post(self) :
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        parser.add_argument('fullname', location='json', required=True)
        parser.add_argument('address', location='json', required=True)
        parser.add_argument('contact', location='json', required=True)
        parser.add_argument('sex', location='json', choices=('F', 'M'), required=True)
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
        db.session.flush()
        bio = Bios(args['fullname'], args['address'], args['contact'], args['sex'], user.id)

        db.session.add(bio)
        db.session.commit()

        app.logger.debug('DEBUG : %s', user)
        app.logger.debug('DEBUG : %s', bio)

        rows = [
            marshal(user, Users.response_fields),
            marshal(bio, Bios.response_fields)
        ]

        return rows, 200

api.add_resource(RegisterResource, '')


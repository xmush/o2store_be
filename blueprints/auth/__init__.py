from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from ..user.model import Users

from blueprints import admin_required

import hashlib

bp_auth = Blueprint('auth', __name__)
api = Api(bp_auth)

class CreateTokenResource(Resource) :
    # @cross_origin(headers=['Content-Type','Authorization'])
    def post(self) :
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        args = parser.parse_args()

        data = Users.query.filter_by(username=args['username']).first()

        if(data == None) :
            return {'status' : '404 NOT FOUND', 'message' : 'username not found, register plis!!'}, 404
        else :

            user_salt = data.salt

            pass_enc = ('%s%s' % (args['password'], user_salt)).encode('utf-8')

            pass_hash = hashlib.sha512(pass_enc).hexdigest()

            if pass_hash == data.password :

                user_data =  marshal(data, Users.jwt_claim_fields)

                token = create_access_token(identity=data.username, user_claims=user_data, fresh=True)

                return {'id' : data.id,'token' : token}, 200
            
            else :
                return {'status' : 'UNAUTHORIZED', 'message' : 'Invalid key or secret'}, 401

class RefreshTokenResource(Resource) :

    # @jwt_required
    @admin_required
    def get(self) :
        current_user = get_jwt_identity()
        token = create_access_token(identity=current_user)
        return {'token' : token}, 200

api.add_resource(CreateTokenResource, '')
api.add_resource(RefreshTokenResource, '/refresh')

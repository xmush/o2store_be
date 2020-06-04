import requests
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal
from blueprints import app
from flask_jwt_extended import jwt_required

bp_weather = Blueprint('weather', __name__)
api = Api(bp_weather)

class PublicGetCurrentWeather(Resource) :

    host = app.config['WIO_HOST']
    key = app.config['WIO_KEY']

    @jwt_required
    def get(self) :

        parser = reqparse.RequestParser()
        parser.add_argument('ip', location='args', default=None)
        args = parser.parse_args()

        rq_get = requests.get(self.host+'curent/ip', params={'ip' : args['ip'], 'key' : self.key})

        # geo = rq_get.json()

        # lat = geo['latitude']
        # lon = geo['longitude']

        # rq = requests.get(self.host + '/current', params={'lat': lat, 'lon': lon, 'key': self.key})
        current = rq_get.json()['data'][0]
        print(rq_get.json())
        # return current['city_name']
        return {
            'city': current['city_name'],
            'country_code': current['country_code'],
            'timezone': current['timezone'],
            'current_weather': current['weather']
        }

api.add_resource(PublicGetCurrentWeather, '/ip')
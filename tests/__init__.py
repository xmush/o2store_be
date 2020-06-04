import pytest, logging, random, string
from flask import Flask, request, json
from blueprints import app, cache
from blueprints.client.model import Clients
from blueprints import db
import hashlib, uuid

def call_client(requests) :
    client = app.test_client()
    # wheather = app.test_weather()
    return client

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))
    
@pytest.fixture
def init_database() :

    db.drop_all()

    db.create_all()

    strdata = 'rahasia0'
    strdata2 = 'rahasia1'

    salt = uuid.uuid4().hex
    hs = ('%s%s' % (strdata, salt)).encode('utf-8')
    clientsec = hashlib.sha512(hs).hexdigest()
    randstr = clientsec.encode('utf-8')

    client1 = Clients(status=1, client_secret=randstr, client_key=strdata, salt=salt, password=randstr)

    hs2 = ('%s%s' % (strdata2, salt)).encode('utf-8')
    clientsec2 = hashlib.sha512(hs2).hexdigest()
    randstr2 = clientsec2.encode('utf-8')

    client2 = Clients(status=0, client_secret=randstr2, client_key=strdata2, salt=salt, password=randstr2)

    db.session.add(client1)
    db.session.add(client2)

    db.session.commit()

@pytest.fixture
def client(request) :
    return call_client(request)

def create_token() :
    token = cache.get('test-token')
    if token is None :
        data = {
            'client_key' : 'rahasia0',
            'client_secret' : 'rahasia0'
        }

        req = call_client(request) 
        res = req.get('/auth', query_string=data)

        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json)

        assert res.status_code == 200

        cache.set('test-token', res_json['token'], timeout=60)

        return res_json['token']
    else :
        return token

def create_internal_token() :
    token = cache.get('test-token-internal')
    if token is None :
        data = {
            'client_key' : 'rahasia1',
            'client_secret' : 'rahasia1'
        }

        req = call_client(request) 
        res = req.get('/auth', query_string=data)

        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json)

        assert res.status_code == 200

        cache.set('test-token-internal', res_json['token'], timeout=60)

        return res_json['token']
    else :
        return token
import json, random, string
from . import app, client, cache, create_token, create_internal_token, logging, init_database

client_id = '0'

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

class TestClientCrud :

    def test_client_list(self, client, init_database) :
        token = create_internal_token()
        data = {
            'p' : 1,
            'rp' : 10,
            'orderby' : 'status',
            'sort' : 'desc' 
        }
        res = client.get('/client/list', headers= {'Authorization' : 'Bearer ' + token}, query_string = data, content_type='application/json')

        res_json = json.loads(res.data)
        
        assert res.status_code == 403

    def test_client_list_internal(self, client, init_database) :
        token = create_token()
        data = {
            'p' : 1,
            'rp' : 10,
            'orderby' : 'status',
            'sort' : 'desc' 
        }
        res = client.get('/client/list', headers= {'Authorization' : 'Bearer ' + token}, query_string = data, content_type='application/json')

        res_json = json.loads(res.data)
        
        assert res.status_code == 200

    def test_client_list_internal_page_2(self, client, init_database) :
        token = create_token()
        data = {
            'p' : 2,
            'rp' : 10,
            'orderby' : 'status',
            'sort' : 'asc' 
        }
        res = client.get('/client/list', headers= {'Authorization' : 'Bearer ' + token}, query_string = data, content_type='application/json')

        res_json = json.loads(res.data)
        
        assert res.status_code == 200

    def test_post_client(self, init_database, client) :
        token = create_internal_token()
        data = {
            'status' : False,
            'client_secret' : randomString(),
            'client_key' : randomString()
        }

        res = client.post('/client', headers= {'Authorization' : 'Bearer ' + token}, data = data, content_type='application/json')

        res_json = json.loads(res.data)
        
        assert res.status_code == 403

    def test_post_client_internal(self, init_database, client) :
        token = create_token()
        url = '/client'
        data = {
            'status' : False,
            'client_secret' : randomString(),
            'client_key' : randomString()
        }

        res = client.post(url, headers= {'Authorization' : 'Bearer ' + token}, data = json.dumps(data), content_type='application/json')

        res_json = json.loads(res.data)
        
        logging.warning('RESULT : %s', res_json)

        assert res.status_code == 200
        client_id = res_json['id']
        
        

    def test_client_geybyid(self, client, init_database, id='1') :
        token = create_token()
        res = client.get('/client/'+id, headers= {'Authorization' : 'Bearer ' + token}, content_type='application/json')

        res_json = json.loads(res.data)
        
        assert res.status_code == 200

    def test_client_geybyid_404(self, client, init_database, id='0') :
        token = create_token()
        res = client.get('/client/'+id, headers= {'Authorization' : 'Bearer ' + token}, content_type='application/json')

        res_json = json.loads(res.data)
        
        assert res.status_code == 404
    
    def test_client_put(self, client, init_database, id='2') :
        token = create_token()
        data = {
            'status' : False,
            'client_secret' : randomString(),
            'client_key' : randomString()
        }
        res = client.put('/client/'+id, headers= {'Authorization' : 'Bearer ' + token}, data = json.dumps(data), content_type='application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_client_put_404(self, client, init_database, id='0') :
        token = create_token()
        data = {
            'status' : False,
            'client_secret' : randomString(),
            'client_key' : randomString()
        }
        res = client.put('/client/'+id, headers= {'Authorization' : 'Bearer ' + token}, data = json.dumps(data), content_type='application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_client_delete(self, client, init_database) :

        token = create_token()

        res = client.delete('/client/'+'2', headers= {'Authorization' : 'Bearer ' + token}, content_type='application/json')

        assert res.status_code == 200

    def test_client_delete_404(self, client, init_database) :

        token = create_token()

        res = client.delete('/client/'+'0', headers= {'Authorization' : 'Bearer ' + token}, content_type='application/json')

        assert res.status_code == 404

    


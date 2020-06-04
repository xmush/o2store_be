from faker import Faker
import requests, random, json


fake = Faker()


for x in range(100) :
    status = random.choice([True, False])
    rand = random.randrange(1, 100)
    client_secret = 'rahasia' + str(x)
    client_key = 'rahasia' + str(x)
    
    url = "http://0.0.0.0:5000/client"

    # payload = "{\n    \"status\" : \""+str(status)+"\",\n    \"age\" : "+client_secret+",\n    \"client_key\" : \""+client_key+"\"\n}\n"
    # payload = "{\n    \"status\" : \"+status+\",\n    \"client_secret\" : \""+client_secret+"\",\n    \"client_key\" : \""+client_key+"\"\n}\n"
    payload = {
        'status' : status,
        'client_secret' : client_secret,
        'client_key' : client_key
    }

    headers = {
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODczOTgwMzksIm5iZiI6MTU4NzM5ODAzOSwianRpIjoiNTU2ZGJjYTEtZThmZi00M2I2LWE1ODUtMjRkYzY0Njg0OGVlIiwiZXhwIjoxNTg3NDg0NDM5LCJpZGVudGl0eSI6InJhaGFzaWEwIiwiZnJlc2giOnRydWUsInR5cGUiOiJhY2Nlc3MiLCJ1c2VyX2NsYWltcyI6eyJpZCI6MSwic3RhdHVzIjp0cnVlfX0.HzKJaaRxDmmkv18ayF2o3Sfk-s_hbXBIfD9EsnbTljo',
    'Content-Type': 'application/json'
    }
    print(payload)
    response = requests.request("POST", url, headers = headers, data = json.dumps(payload))

    print(response.text.encode('utf8'))
from flask import Blueprint
from blueprints import db, app
import werkzeug, os, requests, json

def sendImageToImgur(imgFile) :
    url = app.config['IMGUR_URL']
    cid = app.config['IMGUR_CID']
    
    payload = {}
    files = [
    ('image', imgFile)
    ]
    ncid = 'Client-ID ' + cid
    headers = {
    'Authorization': ncid
    }

    res = requests.post(url, headers=headers, data = payload, files = files)
    response = res.json()

    link = response['data']['link']

    return link
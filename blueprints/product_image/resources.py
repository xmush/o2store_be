from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal
from sqlalchemy import desc
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints import db, app, admin_required
import werkzeug, os, requests, json
# from blueprints.user.model import Users

import hashlib, uuid


from .model import ProductImg
bp_product_img = Blueprint('product_img', __name__)
api = Api(bp_product_img)

app.config['IMAGE_UPLOADS'] = './storage/uploads/produk'
# app.config['IMAGE_UPLOADS'] = './'

class ProductImgResource(Resource) :   
    def __init__(self) :
        pass
    
    def sendImageToImgur(self, imgFile) :
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


    # @jwt_required
    def get(self, id) : 
        qry = ProductImg.query.get(id) 
        if qry is not None :
            return marshal(qry, ProductImg.response_fields), 200
        return {'status': 'NOT_FOUND'}, 404
    
    # # @internal_required    
    # @jwt_required
    def post(self) :
        # claims = get_jwt_claims()

        parser = reqparse.RequestParser()
        parser.add_argument('img_product', type=werkzeug.datastructures.FileStorage, location='files', required=True)
        parser.add_argument('img_description', location='form')
        parser.add_argument('product_id', location='form', type=int, required=True)
        args=parser.parse_args()

        if args['img_product'] == "":
            return {'data':'', 'message':'No file found', 'status':'error'}, 500

        image_produk = args['img_product']

        if image_produk:
            img_link = self.sendImageToImgur(image_produk)
            img_path = img_link
            
        else :
            return {'data':'', 'message':'Something when wrong', 'status':'error'}, 500

        product_img = ProductImg(img_path, args['img_description'], args['product_id'])
        
        db.session.add(product_img)
        db.session.commit()

        app.logger.debug('DEBUG : %s', product_img)

        return marshal(product_img, ProductImg.response_fields), 200, {'Content-Type': 'application/json'}


    # @jwt_required
    def put(self, id) :

    #     qry = Product.query.get(id)
        
        parser = reqparse.RequestParser()
        parser.add_argument('img_product', type=werkzeug.datastructures.FileStorage, location='files')
        parser.add_argument('img_description', location='form')
        parser.add_argument('product_id', location='form', type=int, required=True)
        args=parser.parse_args()

        data_image = ProductImg.query.get(id)

        if args['img_product'] is not None :
            # IMAGE_FOLDER = app.config['IMAGE_UPLOADS']
            data = os.remove('.'+data_image.img_path)
            # print(data)

        UPLOAD_FOLDER = app.config['IMAGE_UPLOADS']
        image_produk = args['img_product']
        randomstr = uuid.uuid4().hex #get randum string to image filename
        filename = randomstr+'_'+image_produk.filename
        image_produk.save(os.path.join(UPLOAD_FOLDER,filename))
        img_path = UPLOAD_FOLDER.replace('./', '/')+'/'+filename

        data_image.img_path = img_path

        if args['img_description'] is not None :
            data_image.img_desc = args['img_description']

        data_image.product_id = args['product_id']

        db.session.commit()

        app.logger.debug('DEBUG : %s', data_image)

        return marshal(data_image, ProductImg.response_fields), 200, {'Content-Type': 'application/json'}

    # @jwt_required
    def delete(self, id) :
        
        img = ProductImg.query.get(id)

        if img is None :
            return {'status' : 'NOT_FOUND'}, 404

        if os.path.exists('.' + img.img_path) == True :
            os.remove('.' + img.img_path)

        db.session.delete(img)
        db.session.commit()

        return {'status': 'DELETED'}, 200


class ProductImgList(Resource):

    def __init__(self):
        pass
    # # @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('order_by', type=int, location='args', help='invalid orderby value', choices=('produck_id'))
        parser.add_argument('sort', location='args', help='invalid sort value', choices=('desc', 'asc'))
        args = parser.parse_args()

        if args['p'] == 1 :
            offset = 0
        else :
            offset = args['p'] * args['rp'] - args['rp']
        
        qry = ProductImg.query

        if args['order_by'] == 'produck_id' :
            if args['sort'] == 'desc' :
                qry = qry.order_by(desc(ProductImg.produck_id))
            else :
                qry = qry.order_by(ProductImg.produck_id)

        rows = []

        for row in qry.limit(args['rp']).offset(offset).all() :
            rows.append(marshal(row, ProductImg.response_fields)) 
        return rows, 200

        return {'status' : 'ok'}

api.add_resource(ProductImgList, '', '/list')
api.add_resource(ProductImgResource, '', '/<id>')
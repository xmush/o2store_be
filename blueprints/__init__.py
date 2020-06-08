import json, config, os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_jwt_extended import JWTManager, verify_fresh_jwt_in_request, get_jwt_claims
from datetime import timedelta
from functools import wraps
from werkzeug.contrib.cache import SimpleCache
from flask_cors import CORS


cache = SimpleCache()

app = Flask(__name__)
CORS(app, origins="http://localhost:3000", allow_headers=[
    "Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
    supports_credentials=True, intercept_exceptions=False)


@app.route("/")
def hello():
    return {"status": "OK by xmush"}, 200


# CORS(app)
# cors = CORS(app, resources = {
#     r"/*" : {
#         "origins" : "*"
#     }
# })

    # response.headers.add('Access-Control-Allow-Origin', '*')
    # response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
# app.config['CORS_HEADERS'] = 'Content-Type'
# cors.init_app
# CORS(app, support_credentials=True)
# CORS(app, origins='*', support_credentials=True)

flask_env = os.environ.get('FLASK_ENV', 'Production')
if flask_env == "Production" :
    app.config.from_object(config.ProductionConfig)
elif flask_env == "Testing" :
    app.config.from_object(config.TestingConfig)
else :
    app.config.from_object(config.DevelopmentConfig)


# jwt
jwt = JWTManager(app)

# set user claim using decorator || pilih salah satu dengan user claim di auth
# @jwt.user_claims_loader
# def add_claims_loader(identity) :
#     return {
#         'claims' : identity,
#         'identifier' : "ATA BATCH 5"
#     }
# ===================================


# custom decorator
def admin_required(fn) :
    @wraps(fn)
    def wrapper(*args, **kwargs) :
        verify_fresh_jwt_in_request()
        claims = get_jwt_claims()
        if claims['role'] != 'admin':
            return {'status' : 'FORBIDEN', 'message' : 'Access Denied'}, 403
        else :
            return fn(*args, **kwargs)
    return wrapper

#=> to export FLASK_ENV
#=> export FLASK_ENV=Development

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

@app.before_request
def before_request():
    if request.method != 'OPTIONS':  # <-- required
        print(request.method)
        pass
    else :
        #ternyata cors pake method options di awal buat ngecek CORS dan harus di return kosong 200, jadi di akalin gini deh. :D
        return {}, 200, {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'POST, PUT, GET, DELETE', 'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Authorization'}

# add log method
@app.after_request
def after_request(response) :
    # response.headers.add('Access-Control-Allow-Origin', '*')
    # response.headers.add('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization')
    # response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    # response.headers.add('Access-Control-Max-Age', '1000')
    # response.headers.add('Access-Control-Allow-Credentials', 'true')
    try:
        reqData = request.get_json()
    except Exception as e:
        reqData = request.args.to_dict()
    if response.status_code == 200 :
        app.logger.warning("REQUEST_LOG\t%s", json.dumps({
        'method' : request.method,
        'code' : response.status,
        'uri' : request.full_path,
        'request' : reqData, 
        'response' : json.loads(response.data.decode('utf-8'))}))
    else :
        app.logger.error("REQUEST_LOG\t%s", json.dumps({
        'method' : request.method,
        'code' : response.status,
        'uri' : request.full_path,
        'request' : reqData, 
        'response' : json.loads(response.data.decode('utf-8'))}))

    return response

from blueprints.client.resources import bp_client
from blueprints.user.resources import bp_user
from blueprints.bio.resources import bp_bio
from blueprints.category.resources import bp_category
from blueprints.product.resources import bp_product
from blueprints.product_image.resources import bp_product_img
from blueprints.product_coment.resources import bp_product_comment
from blueprints.product_like.resources import bp_product_like
from blueprints.cart.resources import bp_cart
from blueprints.transaction.resources import bp_transaction
from blueprints.transaction_detail.resources import bp_transaction_detail
from blueprints.shipping.resources import bp_shipping
from blueprints.public.register import bp_register
from blueprints.user_actions import bp_user_product
from blueprints.user_transaction import bp_user_transaction
from blueprints.auth import bp_auth

app.register_blueprint(bp_client, url_prefix='/client')
app.register_blueprint(bp_user, url_prefix='/user')
app.register_blueprint(bp_bio, url_prefix='/bio')
app.register_blueprint(bp_category, url_prefix='/category')
app.register_blueprint(bp_product, url_prefix='/product')
app.register_blueprint(bp_product_img, url_prefix='/product_img')
app.register_blueprint(bp_product_comment, url_prefix='/product_comment')
app.register_blueprint(bp_product_like, url_prefix='/product_like')
app.register_blueprint(bp_cart, url_prefix='/cart')
app.register_blueprint(bp_transaction, url_prefix='/transaction')
app.register_blueprint(bp_transaction_detail, url_prefix='/transaction_detail')
app.register_blueprint(bp_shipping, url_prefix='/shipping')
app.register_blueprint(bp_register, url_prefix='/registration')
app.register_blueprint(bp_user_product, url_prefix='/user/product')
app.register_blueprint(bp_user_transaction, url_prefix='/user/transaction')
app.register_blueprint(bp_auth, url_prefix='/auth')

db.create_all()

from flask import Flask, request
from flask_restful import Resource, Api
import json, logging, sys
from logging.handlers import RotatingFileHandler

from blueprints import app, manager
# app = Flask(__name__)

api = Api(app, catch_all_404s=True)

# # from blueprints.client.resources import bp_client

# # setting mysql connection
# app.config['APP_DEBUG'] = True
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@toor@0.0.0.0:3306/rest_api'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# manager = Manager(app)
# manager.add_command('db', MigrateCommand)

# # app.register_blueprint(bp_client, url_prefix='/client')

# # add log method
# @app.after_request
# def after_request(response) :
#     try:
#         reqData = request.get_json()
#     except Exception as e:
#         reqData = request.args.to_dict()
#     if response.status_code == 200 :
#         app.logger.warning("REQUEST_LOG\t%s", json.dumps({
#         'method' : request.method,
#         'code' : response.status,
#         'uri' : request.full_path,
#         'request' : reqData, 
#         'response' : json.loads(response.data.decode('utf-8'))}))
#     else :
#         app.logger.error("REQUEST_LOG\t%s", json.dumps({
#         'method' : request.method,
#         'code' : response.status,
#         'uri' : request.full_path,
#         'request' : reqData, 
#         'response' : json.loads(response.data.decode('utf-8'))}))

#     # if request.method == 'GET' :
#     #     app.logger.warning("REQUEST_LOG\t%s", json.dumps({'request' : request.args.to_dict(), 'response' : json.loads(response.data.decode('utf-8'))}))
#     # else :
#     #     app.logger.warning("REQUEST_LOG\t%s", json.dumps({'request' : request.get_json(), 'response' : json.loads(response.data.decode('utf-8'))}))

#     return response

if __name__ == '__main__' :
    # defini log format
    try :
        if sys.argv[1] == 'db' :
            manager.run()
    except Exception as e :
        formatter = logging.Formatter("[%(asctime)s]{%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
        log_handler = RotatingFileHandler("%s/%s" % (app.root_path, '../storage/log/app.log'), maxBytes=10000, backupCount=10)
        log_handler.setLevel(logging.INFO)
        log_handler.setFormatter(formatter)
        app.logger.addHandler(log_handler)

        app.run(debug=app.config['DEBUG'], host=app.config['HOST'], port=app.config['PORT'])
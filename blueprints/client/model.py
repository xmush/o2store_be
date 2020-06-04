from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime

class Clients(db.Model) :
    __tabelname__ = "client"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # name = db.Column(db.String(50), nullable=True)
    status = db.Column(db.Boolean, nullable=False)
    client_secret = db.Column(db.String(200), nullable=False)
    client_key = db.Column(db.String(200), unique=True ,nullable=False)
    salt = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True)

    response_fields = {
        'id' : fields.Integer,
        'status' : fields.String,
        'client_secret' : fields.String,
        'client_key' : fields.String,
        'salt' : fields.String,
        'password' : fields.String,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime,
        'deleted_at' : fields.DateTime
    }

    jwt_claim_fields = {
        'id' : fields.Integer,
        'status' : fields.Boolean
    }

    def __init__(self, status, client_secret, client_key, salt, password) :
        self.status = status
        self.client_secret = client_secret 
        self.client_key = client_key
        self.salt = salt
        self.password = password

    def __repr__(self) :
        return '<Clients %r>' % self.id
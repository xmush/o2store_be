import configparser
from datetime import timedelta

cfg = configparser.ConfigParser()
cfg.read('.env')

class Config() :
    SQLALCHEMY_DATABASE_URI = '%s+%s://%s:%s@%s:3306/%s' % (
        cfg['database']['default_connection'],
        cfg['mysql']['driver'],
        cfg['mysql']['user'],
        cfg['mysql']['password'],
        cfg['mysql']['host'],
        cfg['mysql']['db']
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    HOST = cfg['app']['host']
    PORT = cfg['app']['port']
    JWT_SECRET_KEY = cfg['jwt']['key']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=int(cfg['jwt']['time_live']))

    IMGUR_CID = cfg['imgur']['cid']
    IMGUR_SEC = cfg['imgur']['csecret']
    IMGUR_URL = cfg['imgur']['url']


class DevelopmentConfig(Config) :
    APP_DEBUG =True
    DEBUG = True


class ProductionConfig(Config) :
    APP_DEBUG = False
    DEBUG = False

class TestingConfig(Config) :
    APP_DEBUG = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = '%s+%s://%s:%s@%s:3306/%s_testing' % (
        cfg['database']['default_connection'],
        cfg['mysql']['driver'],
        cfg['mysql']['user'],
        cfg['mysql']['password'],
        cfg['mysql']['host'],
        cfg['mysql']['db']
    )
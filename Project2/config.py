import os

class Config(object):
    DEBUG = False
    TESTING = False

basedir = os.path.abspath(os.path.dirname(__file__))

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir,"grocery_store.sqlite3")
    SECRET_KEY = 'thisissecret'
    SECURITY_PASSWORD_SALT = 'saltpassword'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_SILENCE_UBER_WARNING = 1
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    CACHE_TYPE = "redis"
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0
    CACHE_REDIS_URL = "redis://localhost:6379"  
    CACHE_DEFAULT_TIMEOUT = 300
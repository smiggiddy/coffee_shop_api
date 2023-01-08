import os

class Config(object):
    Testing = False 


class DevConfig(Config):    
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "coffee_shop.db")
    DEBUG = True 
    PORT = 5050
    FLASK_RUN_PORT = 5050
    SECRET_KEY = 'MakeMFinMoneyBatch'


class TestConfig(Config):
    Testing = True 
    basedir = os.path.abspath(os.path.dirname(__file__))
    # move test database into tests folder
    sub_dir = os.path.abspath(os.path.dirname(basedir) + '/tests')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(sub_dir, "test.db")
    SECRET_KEY = 'DevTesting'

from .config import DevConfig, TestConfig
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import os


db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
limiter = Limiter( key_func=get_remote_address)


def create_app(test_config=None):
    app = Flask(__name__)

    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object(DevConfig())
    else:
        # load the test config if passed in
        app.config.from_object(test_config)


    # init plugins 
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    

    # import API routes and register 
    from .api_views import api_views
    app.register_blueprint(api_views, url_prefix='/api/v1')





    # ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # import the db models before creating the database
    from .models import  Products, Orders, OrderItems

    with app.app_context():
        db.create_all()

    @app.cli.command('db_drop')
    def db_drop():
        db.drop_all()
        print('Database dropped!')



    return app



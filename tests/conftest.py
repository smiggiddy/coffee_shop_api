from coffee_shop import create_app, TestConfig, db
from coffee_shop.models import Products
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token
import os
import pytest 





@pytest.fixture()
def app():
    app = create_app(test_config=TestConfig()) 

    # setup test db entry

    yield app

    # clean up / reset resources here
    with app.app_context():
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

@pytest.fixture()
def jwt_token(app):

    with app.app_context():
        access_token = create_access_token('testuser')

    return access_token


@pytest.fixture()
def db_session(app, request):
    with app.app_context():
        db.create_all()
        yield db.session
        db.session.remove()
        db.drop_all()




# def cleanup():
#     basedir = os.path.abspath(os.path.dirname(__file__))
#     db_file = os.path.join(basedir, 'test.db')

#     if os.path.exists(db_file):
#         os.remove(db_file)



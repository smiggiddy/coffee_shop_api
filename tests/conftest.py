from coffee_shop import create_app, TestConfig, db
from flask_jwt_extended import create_access_token
import pytest 





@pytest.fixture()
def app():
    app = create_app(test_config=TestConfig()) 
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
        # app.extensions["sqlalchemy"].create_all()
        # yield app.extensions["sqlalchemy"].session
        # app.extensions["sqlalchemy"].remove()
        # app.extensions["sqlalchemy"].drop_all()
        db.create_all()
        yield db.session
        db.session.remove()
        db.drop_all()


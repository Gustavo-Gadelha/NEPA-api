import pytest
from sqlalchemy.orm import sessionmaker, scoped_session

from app import create_app, db as _db


@pytest.fixture(scope='session')
def app():
    app = create_app('testing')
    with app.app_context():
        yield app


@pytest.fixture(scope='session')
def db(app):
    _db.create_all()
    yield _db
    _db.session.rollback()
    _db.session.close()
    _db.drop_all()


@pytest.fixture
def db_session(db):
    Session = scoped_session(sessionmaker(bind=db.engine))

    try:
        yield Session()
    finally:
        Session.remove()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()

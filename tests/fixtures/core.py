import pytest
from sqlalchemy.orm import sessionmaker

from app import create_app
from app.extensions import db as _db


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


@pytest.fixture(scope="function")
def db_session(db):
    Session = sessionmaker(bind=db.engine)
    with db.engine.connect() as connection:
        transaction = connection.begin()
        session = Session(bind=connection)

        try:
            yield session
        finally:
            session.close()
            transaction.rollback()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()

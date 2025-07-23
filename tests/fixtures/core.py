import pytest
from sqlalchemy.orm import sessionmaker

from app import create_app
from app.extensions import db as _db


@pytest.fixture
def app():
    app = create_app('testing')
    yield app


@pytest.fixture
def db(app):
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.rollback()
        _db.session.close()
        _db.drop_all()


@pytest.fixture
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

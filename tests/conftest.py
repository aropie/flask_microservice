import pytest

from app import create_app, db
from app.models import UserAccount


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app(True)
    yield app


@pytest.fixture
def init_db(app):
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield db
        db.session.close()


@pytest.fixture
def create_users(init_db):
    # PASSWORD: 'nocontabanconmiastucia',
    user1 = UserAccount(
        id=99,
        first_name='Roberto',
        father_surname='Gomez',
        mother_surname='Bolañoz',
        gender='M',
        email='chespirito@example.com',
        birth_date='1929-02-21',
        cellphone='5514632156',
        salt='$6$xCHIfAYEYR2uN2vy',
        hashed_password='pbkdf2:sha256:150000$Pdwux4CrvfEq5tto'
        '$b6059e8ee60837d290bf024b72d7cc3cebb105024a05413a6c4ebdc5c6ed0e0d'
    )
    db.session.add(user1)
    db.session.commit()
    db.session.close()


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

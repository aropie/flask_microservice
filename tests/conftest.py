import pytest

from app import create_app, db
from init_data import init_test_data


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    db_path = 'postgresql://postgres:@localhost/user_service_test'
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': db_path,
                      'SQLALCHEMY_TRACK_MODIFICATIONS': True,
                      'SECRET_KEY': 'testing'})

    with app.app_context():
        db.drop_all()
        db.create_all()
        init_test_data()
        yield app
        db.session.close()


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

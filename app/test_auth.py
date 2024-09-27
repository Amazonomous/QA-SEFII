import pytest
from werkzeug.security import generate_password_hash, check_password_hash
from app import create_app, db
from app.models import User
import os

@pytest.fixture
def app():
    os.environ['DATABASE_URL'] = 'sqlite://'
    app = create_app()
    with app.app_context():
        db.create_all()
    yield app
    db.session.remove()
    db.drop_all()
    app.app_context.pop()


@pytest.fixture
def client(app):
    app.app_context = app.app_context()
    app.app_context.push()
    return app.test_client()

def test_invalid_login_user_does_not_exist(client):
    # Create a user
    user = User(email="user@example.com", username="user", password=generate_password_hash(
                    "user1234", method='scrypt'))
    db.session.add(user)
    db.session.commit()
    
    # Login with invalid credentials
    response = client.post('/login', data=dict(
        email='test@example.com',
        password='test1234'
    ), follow_redirects=True)

    # We should've not found a user
    assert response.status_code == 200
    assert b'User does not exist' in response.data

def test_invalid_login_incorrect_password(client):
    # Create a user
    user = User(email="test@example.com", username="test", password=generate_password_hash(
                    "test1234", method='scrypt'))
    db.session.add(user)
    db.session.commit()
    
    # Login with incorrect credentials
    response = client.post('/login', data=dict(
        email='test@example.com',
        password='test4321'
    ), follow_redirects=True)

    # We should've not logged in successfully
    assert response.status_code == 200
    assert b'Incorrect login details, please try again' in response.data

def test_valid_login(client):
    # Create a user
    user = User(email="test@example.com", username="test", password=generate_password_hash(
                    "test1234", method='scrypt'))
    db.session.add(user)
    db.session.commit()
    
    # Login with correct credentials
    response = client.post('/login', data=dict(
        email='test@example.com',
        password='test1234'
    ), follow_redirects=True)

    # We should've logged in successfully
    assert response.status_code == 200
    assert check_password_hash(user.password, "test1234") # Check we're hashing successfully
    assert b'Logged in successfully' in response.data
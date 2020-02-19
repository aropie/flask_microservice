import pytest
import json

BASE_URL = '/api/v1/auth'


@pytest.mark.parametrize('path, payload', (
    pytest.param('/register', {
        'middle_name': 'Roberto',
        'gender': 'F',
        'father_surname': 'Lopez',
        'mother_surname': 'Martinez',
        'email': 'someemail@example.com',
        'birth_date': '2019-01-01',
        'cellphone': '5529464306',
        'password': 'superbadpass'
        }, id='Missing first name'),
    pytest.param('/register', {
        'first_name': 'Juan',
        'middle_name': 'Roberto',
        'gender': 'F',
        'mother_surname': 'Martinez',
        'email': 'someemail@example.com',
        'birth_date': '2019-01-01',
        'cellphone': '5529464306',
        'password': 'superbadpass'
        }, id='Missing father_surname'),
    pytest.param('/register', {
        'first_name': 'Juan',
        'middle_name': 'Roberto',
        'gender': 'F',
        'father_surname': 'Lopez',
        'email': 'someemail@example.com',
        'birth_date': '2019-01-01',
        'cellphone': '5529464306',
        'password': 'superbadpass'
        }, id='Missing mother_surname'),
    pytest.param('/register', {
        'first_name': 'Juan',
        'middle_name': 'Roberto',
        'gender': 'F',
        'father_surname': 'Lopez',
        'mother_surname': 'Martinez',
        'birth_date': '2019-01-01',
        'cellphone': '5529464306',
        'password': 'superbadpass'
        }, id='Missing email'),
    pytest.param('/register', {
        'first_name': 'Juan',
        'middle_name': 'Roberto',
        'gender': 'F',
        'father_surname': 'Lopez',
        'mother_surname': 'Martinez',
        'email': 'someemail@example.com',
        'cellphone': '5529464306',
        'password': 'superbadpass'
        }, id='Missing birth_date'),
    pytest.param('/register', {
        'first_name': 'Juan',
        'middle_name': 'Roberto',
        'gender': 'F',
        'father_surname': 'Lopez',
        'mother_surname': 'Martinez',
        'email': 'someemail@example.com',
        'birth_date': '2019-01-01',
        'password': 'superbadpass'
        }, id='Missing cellphone'),
    pytest.param('/register', {
        'first_name': 'Juan',
        'middle_name': 'Roberto',
        'gender': 'F',
        'father_surname': 'Lopez',
        'mother_surname': 'Martinez',
        'email': 'someemail@example.com',
        'birth_date': '2019-01-01',
        'cellphone': '5529464306',
        }, id='Missing password'),
    pytest.param('/register', {
        'first_name': 'Juan',
        'middle_name': 'Roberto',
        'father_surname': 'Lopez',
        'mother_surname': 'Martinez',
        'email': 'someemail@example.com',
        'birth_date': '2019-01-01',
        'cellphone': '5529464306',
        'password': 'superbadpass'
        }, id='Missing gender'),
    pytest.param('/login', {
        'email': 'someemail@example.com',
    }, id='Missing password'),
    pytest.param('/login', {
        'password': 'someemail@example.com',
    }, id='Missing password'),
     ))
def test_missing_argument(client, path, payload):
    url = BASE_URL + path
    rv = client.post(url, json=payload)
    assert rv.status_code == 400


def test_register_user(client):
    """Tests that users are created correctly."""
    payload = {
        'first_name': 'Juan',
        'middle_name': 'Roberto',
        'gender': 'F',
        'father_surname': 'Lopez',
        'mother_surname': 'Martinez',
        'email': 'someemail@example.com',
        'birth_date': '2019-01-01',
        'cellphone': '5529464306',
        'password': 'superbadpass'
    }

    rv = client.post('/api/v1/auth/register', json=payload)

    assert rv.status_code == 201
    # Remove password since it's not expected in the response
    payload.pop('password')

    for key, value in payload.items():
        assert rv.json[key] == value


def test_register_user_repeated_email(client):
    """Tests an error is raised when creating a user with repeated email."""
    payload = {
        'first_name': 'Juan',
        'middle_name': 'Roberto',
        'gender': 'F',
        'father_surname': 'Lopez',
        'mother_surname': 'Martinez',
        'email': 'chespirito@example.com',
        'birth_date': '2019-01-01',
        'cellphone': '5529464306',
        'password': 'superbadpass'
    }
    rv = client.post('/api/v1/auth/register', json=payload)

    assert rv.status_code == 409


def test_login(client):
    """Tests that a token is successfully generated."""
    payload = {
        'email': 'chespirito@example.com',
        'password': 'nocontabanconmiastucia',
    }

    url = BASE_URL + '/login'
    rv = client.post(url, json=payload)

    assert rv.status_code == 200
    assert rv.json.get('token_type') == 'bearer'
    assert 'access_token' in rv.json

def test_login_incorrect_pasword(client):
    """Tests that a incorrect password throws a 401."""
    payload = {
        'email': 'chespirito@example.com',
        'password': 'badpassword',
    }

    url = BASE_URL + '/login'
    rv = client.post(url, json=payload)

    assert rv.status_code == 401


def test_login_incorrect_email(client):
    """Tests that an incorrect email throws a 401."""
    payload = {
        'email': 'bademail@example.com',
        'password': 'nocontabanconmiastucia',
    }

    url = BASE_URL + '/login'
    rv = client.post(url, json=payload)

    assert rv.status_code == 401


def test_try_restricted_endpoint_without_token(client):
    """Tests that accessing a restricted endpoint is forbidden"""
    url = BASE_URL + '/test'
    rv = client.get(url)

    assert rv.status_code == 401


def test_access_restricted_endpoint_with_token(client):
    """Tests accessing a restricted endpoint with token"""
    payload = {
        'email': 'chespirito@example.com',
        'password': 'nocontabanconmiastucia',
    }

    login_url = BASE_URL + '/login'
    rv = client.post(login_url, json=payload)
    token = rv.json.get('access_token')

    restricted_url = BASE_URL + '/test'
    rv = client.get(restricted_url,
                    headers={'Authentication': f'Bearer {token}'})

    assert rv.status_code == 200

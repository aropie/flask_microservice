from flask import request, g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask_restx import Resource, Namespace

from sqlalchemy.orm.exc import NoResultFound
import voluptuous as v
import voluptuous.error as verr
import voluptuous.humanize as vhum
from werkzeug.exceptions import BadRequest, Conflict, Unauthorized

from app.models.user_account import UserAccountSchema
from app.models import UserAccount
from app import db
from app.apis.users import Users

api = Namespace('auth', description='Authentication related operations')
basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@api.route('/register')
class Register(Resource):
    REGISTER_VALIDATOR = Users.USER_VALIDATOR.extend({
        'password': str,
    }, required=True)

    @api.doc(responses={
        201: 'User created',
        400: 'Validation Error',
        409: 'Email already taken',
    })
    def post(self):
        try:
            vhum.validate_with_humanized_errors(request.json,
                                                self.REGISTER_VALIDATOR)
        except verr.Error as invalid:
            raise BadRequest(str(invalid))

        email = request.json['email']
        user_with_same_email = UserAccount.query.filter(
            UserAccount.email == email
        ).one_or_none()
        if user_with_same_email:
            raise Conflict(f"Email '{email}' is already taken.")

        password = request.json.pop('password')
        new_user = UserAccount(**request.json)
        new_user.hash_password(password)
        db.session.add(new_user)
        db.session.commit()

        schema = UserAccountSchema()
        return schema.dump(new_user), 201


@api.route('/login')
class Login(Resource):
    LOGIN_VALIDATOR = v.Schema({
        'email': v.Email(),
        'password': str
    }, required=True)

    @api.doc(responses={
        200: 'Token generated',
        400: 'Validation error',
        401: 'Unauthorized',
    })
    def post(self):
        try:
            vhum.validate_with_humanized_errors(request.json,
                                                self.LOGIN_VALIDATOR)
        except verr.Error as invalid:
            raise BadRequest(str(invalid))

        try:
            user = UserAccount.query.filter_by(
                email=request.json.get('email')).one()
        except NoResultFound:
            raise Unauthorized('Email or password incorrect')
        if not user.verify_password(request.json.get('password')):
            raise Unauthorized('Email or password incorrect')

        token = user.generate_auth_token()
        payload = {
            'token_type': 'bearer',
            'access_token': token.decode('ascii'),
            'expires_in': 600,
            'refresh_token': 'TODO',
        }
        return payload


@api.route('/test')
class ProtectedEndpoint(Resource):
    @token_auth.login_required
    @api.doc(security='tokenAuth')
    def get(self):
        return 'YAS!'


@token_auth.verify_token
def verify_token(token):
    user = UserAccount.verify_auth_token(token)
    return bool(user)


@basic_auth.verify_password
def verify_password(username, password):
    user = UserAccount.verify_auth_token(username)
    try:
        user = UserAccount.query.filter_by(email=username).one()
    except NoResultFound:
        return False
    if not user.verify_password(password):
        return False
    g.user = user
    return True

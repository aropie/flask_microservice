from flask import request, g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask_restx import Resource, Namespace, fields

from sqlalchemy.orm.exc import NoResultFound
import voluptuous as v
import voluptuous.error as verr
import voluptuous.humanize as vhum
from werkzeug.exceptions import BadRequest, Conflict, Unauthorized

from app.models import UserAccount
from app import db
from app.apis.users import Users, base_user_model, user_model

api = Namespace('auth', description='Authentication related operations')
basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


register_model = api.clone('Register', base_user_model, {
    'password': fields.String(required=True, discriminator=True),
})

login_model = api.model('Login', {
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})

token_model = api.model('Token', {
    'token_type': fields.String(default='bearer'),
    'access_token': fields.String(),
    'expires_in': fields.Integer(default=600),
})


@api.route('/register')
class Register(Resource):
    REGISTER_VALIDATOR = Users.USER_VALIDATOR.extend({
        'password': str,
    }, required=True)

    @api.doc(responses={
        400: 'Validation Error',
        409: 'Email already taken',
    }, body=register_model)
    @api.marshal_with(user_model, skip_none=True,
                      code=201, description='User created')
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

        return new_user, 201


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
    }, body=login_model)
    @api.marshal_with(token_model)
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
        return {'access_token': token.decode('ascii')}


@api.route('/test')
class ProtectedEndpoint(Resource):
    @token_auth.login_required
    @api.doc(security='tokenAuth')
    def get(self):
        return 'Token correct. Access granted!'


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

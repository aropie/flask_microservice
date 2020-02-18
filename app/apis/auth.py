from flask import request, g
from flask_httpauth import HTTPBasicAuth
from flask_restplus import Resource, Namespace

from sqlalchemy.orm.exc import NoResultFound
import voluptuous.error as verr
import voluptuous.humanize as vhum
from werkzeug.exceptions import BadRequest, Conflict

from app.models.user import UserAccountSchema
from app.models import UserAccount
from app.db import DB
from app.apis.users import Users

api = Namespace('auth', description='Authentication related operations')
auth = HTTPBasicAuth()


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
        DB.session.add(new_user)
        DB.session.commit()

        schema = UserAccountSchema()
        return schema.dump(new_user), 201


@api.route('/token')
class GenerateToken(Resource):
    @api.doc(responses={
        200, 'Token generated',
        401, 'Unauthorized',
    })
    @auth.login_required
    def get(self):
        token = g.user.generate_auth_token()
        return {'token': token.decode('ascii')}


@auth.verify_password
def verify_password(username_or_token, password):
    # Try to authenticate with token
    print(username_or_token, password)
    user = UserAccount.verify_auth_token(username_or_token)
    if not user:
        # If no token, try to authenticate with user:pwd
        try:
            user = UserAccount.query.filter_by(email=username_or_token).one()
        except NoResultFound:
            return False
        if not user.verify_password(password):
            return False
    g.user = user
    return True

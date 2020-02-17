import functools

from flask import Blueprint, jsonify, request, g
from flask_httpauth import HTTPBasicAuth
from sqlalchemy.orm.exc import NoResultFound
import voluptuous as v
import voluptuous.error as verr
import voluptuous.humanize as vhum

from app.models.user import UserAccountSchema
from app.models import UserAccount
from app.db import DB
from app.users import USER_VALIDATOR


REGISTER_VALIDATOR = USER_VALIDATOR.extend({
    'password': str,
}, required=True)

LOGIN_VALIDATOR = v.Schema({
    'email': v.Email(),
    'password': str
}, required=True)

bp = Blueprint('auth', __name__, url_prefix='/v1/auth')
auth = HTTPBasicAuth()


@bp.route('/register', methods=('POST',))
def register():
    try:
        vhum.validate_with_humanized_errors(request.json,
                                            REGISTER_VALIDATOR)
    except verr.Error as invalid:
        return jsonify({'message': str(invalid)}), 400

    email = request.json['email']
    user_with_same_email = UserAccount.query.filter(
        UserAccount.email == email
    ).one_or_none()
    if user_with_same_email:
        return jsonify({'message': f'Email "{email}" is already taken.'}), 409

    password = request.json.pop('password')
    new_user = UserAccount(**request.json)
    new_user.hash_password(password)
    DB.session.add(new_user)
    DB.session.commit()

    schema = UserAccountSchema()
    return schema.dumps(new_user)


@bp.route('/blah', methods=('GET', ))
@auth.login_required
def blah():
    return 'Success!'


@bp.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


@auth.verify_password
def verify_password(username_or_token, password):
    # Try to authenticate with token
    user = UserAccount.verify_auth_token(username_or_token)
    if not user:
        # If not token, try to authenticate with user:pwd
        try:
            user = UserAccount.query.filter_by(email=username_or_token).one()
        except NoResultFound:
            return False
        if not user.verify_password(password):
            return False
    g.user = user
    return True

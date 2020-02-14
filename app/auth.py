import functools

from flask import Blueprint, jsonify, request

import voluptuous as v
import voluptuous.error as verr
import voluptuous.humanize as vhum

from app.models.user import UserAccountSchema
from app.models import UserAccount, Credentials
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
    new_user.save_password(password)
    DB.session.add(new_user)
    DB.session.commit()

    schema = UserAccountSchema()
    return schema.dumps(new_user)


@bp.route('/login', methods=('POST',))
def login():
    try:
        vhum.validate_with_humanized_errors(request.json,
                                            LOGIN_VALIDATOR)
    except verr.Error as invalid:
        return jsonify({'message': str(invalid)}), 400

    email = request.json['email']
    creds = Credentials.query.get(email)
    if not creds:
        return jsonify({'message': f'Invalid email'})

    if not creds.is_password_correct(request.json['password']):
        return jsonify({'message': 'Incorrect email or password'}), 403

    return 'Access Granted'


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        pass

    return wrapped_view

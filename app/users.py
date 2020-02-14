from flask import Blueprint, request, jsonify

import voluptuous as v
import voluptuous.error as verr
import voluptuous.humanize as vhum

from app.models.user import UserAccount, UserAccountSchema
from app.db import DB

USER_VALIDATOR = v.Schema({
    'first_name': v.All(str, v.Length(min=1)),
    v.Optional('middle_name'): v.All(str, v.Length(min=1)),
    'father_surname': v.All(str, v.Length(min=1)),
    'mother_surname': v.All(str, v.Length(min=1)),
    'email': v.Email(),
    'birth_date': v.Date(),
    'cellphone': v.All(str, v.Length(min=10, max=10)),
}, required=True)


bp = Blueprint('users', __name__, url_prefix='/v1/users')


@bp.route('/', methods=('GET', 'POST'))
def users():
    if request.method == 'POST':
        try:
            vhum.validate_with_humanized_errors(request.json,
                                                USER_VALIDATOR)
        except verr.Error as invalid:
            return jsonify({'message': str(invalid)}), 400

        new_user = UserAccount(**request.json)
        DB.session.add(new_user)
        DB.session.commit()
        schema = UserAccountSchema()
        return schema.dumps(new_user)
    elif request.method == 'GET':
        users = UserAccount.query.all()
        schema = UserAccountSchema(many=True)
        return schema.dumps(users)

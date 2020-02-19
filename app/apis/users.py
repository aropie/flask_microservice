from flask import request
from flask_restx import Resource, Namespace, fields, Model

import voluptuous as v
import voluptuous.error as verr
import voluptuous.humanize as vhum
from werkzeug.exceptions import BadRequest

from app.models import UserAccount
from app import db


api = Namespace('v1/users', description='User related operations')

base_user_model = api.model('UserAccount', {
    'first_name': fields.String(required=True),
    'middle_name': fields.String(),
    'father_surname': fields.String(required=True),
    'mother_surname': fields.String(required=True),
    'gender': fields.String(required=True, enum=['M', 'F', 'O', 'U']),
    'email': fields.String(required=True),
    'birth_date': fields.Date(required=True),
    'cellphone': fields.String(required=True),
})

input_user_model = api.clone('UserAccountInput', base_user_model, {
    'password': fields.String(required=True, discriminator=True),
})

output_user_model = api.clone('UserAccountOutput', base_user_model, {
    'id': fields.Integer(discriminator=True),
})


class Users(Resource):

    USER_VALIDATOR = v.Schema({
        'first_name': v.All(str, v.Length(min=1)),
        v.Optional('middle_name'): str,
        'father_surname': v.All(str, v.Length(min=1)),
        'mother_surname': v.All(str, v.Length(min=1)),
        'gender': v.In(['M', 'F', 'O', 'U'],
                       "Allowed values 'M', 'F', 'O', 'U'"),
        'email': v.Email(),
        'birth_date': v.Date(),
        'cellphone': v.All(str, v.Length(min=10, max=10)),
    }, required=True)

    def get(self):
        users = UserAccount.query.all()
        schema = UserAccountSchema(many=True)
        return schema.dumps(users)

    def post(self):
        try:
            vhum.validate_with_humanized_errors(request.json,
                                                self.USER_VALIDATOR)
        except verr.Error as invalid:
            raise BadRequest(str(invalid))

        new_user = UserAccount(**request.json)
        db.session.add(new_user)
        db.session.commit()
        schema = UserAccountSchema()
        return schema.dumps(new_user)

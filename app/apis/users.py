from flask import request
from flask_restx import Resource, Namespace

import voluptuous as v
import voluptuous.error as verr
import voluptuous.humanize as vhum
from werkzeug.exceptions import BadRequest

from app.models.user import UserAccount, UserAccountSchema
from app.db import DB


api = Namespace('v1/users', description='User related operations')


class Users(Resource):

    USER_VALIDATOR = v.Schema({
        'first_name': v.All(str, v.Length(min=1)),
        v.Optional('middle_name'): v.All(str, v.Length(min=1)),
        'father_surname': v.All(str, v.Length(min=1)),
        'mother_surname': v.All(str, v.Length(min=1)),
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
        DB.session.add(new_user)
        DB.session.commit()
        schema = UserAccountSchema()
        return schema.dumps(new_user)

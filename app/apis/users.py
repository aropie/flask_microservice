from flask_restx import Resource, Namespace, fields

import voluptuous as v

from app.models import UserAccount


api = Namespace('users', description='User related operations')

base_user_model = api.model('BaseUser', {
    'first_name': fields.String(required=True),
    'middle_name': fields.String(),
    'father_surname': fields.String(required=True),
    'mother_surname': fields.String(required=True),
    'gender': fields.String(required=True, enum=['M', 'F', 'O', 'U'],
                            attribute=lambda x: x.gender.name),
    'email': fields.String(required=True),
    'birth_date': fields.Date(required=True),
    'cellphone': fields.String(required=True),
})

user_model = api.clone('UserAccount', base_user_model, {
    'id': fields.Integer(discriminator=True),
})


@api.route('/')
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

    @api.marshal_with(user_model, skip_none=True, as_list=True)
    def get(self):
        users = UserAccount.query.all()
        return users

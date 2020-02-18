from flask import Blueprint
from flask_restplus import Api

from app.apis.auth import api as ns_auth
from app.apis.users import api as ns_users

blueprint = Blueprint('api', __name__)
api = Api(blueprint, version='1.0', title='Users API',
          description='A simple Users management API')

api.add_namespace(ns_auth)
api.add_namespace(ns_users)

authorizations = {
    'basic': {
        'type': 'basic',
    }
}
api.authorizations = authorizations

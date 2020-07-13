from flask_restful import Api

from app import *

from .v1.resources.errors import errors

api = Api(app, errors=errors)

# INFO: auth related API resources
from .v1.resources.auth import AuthSignup, AuthLogin, AuthAccessToken, AuthCurrentUser

api.add_resource(AuthSignup, '/api/v1/auth/signup', endpoint='auth_login')
api.add_resource(AuthLogin, '/api/v1/auth/login', endpoint='auth_signup')
api.add_resource(AuthAccessToken, '/api/v1/auth/access-token', endpoint='auth_access_token')
api.add_resource(AuthCurrentUser, '/api/v1/auth/current-user', endpoint='auth_current_user')

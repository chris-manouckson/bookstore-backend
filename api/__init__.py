from flask_restful import Api

from app import *

api = Api(app)

# INFO: auth related API resources
from .v1.auth import AuthSignup, AuthLogin, AuthCurrent, AuthLogout

api.add_resource(AuthSignup, '/api/v1/auth/signup', endpoint='auth_login')
api.add_resource(AuthLogin, '/api/v1/auth/login', endpoint='auth_signup')
api.add_resource(AuthCurrent, '/api/v1/auth/current', endpoint='auth_current')
api.add_resource(AuthLogout, '/api/v1/auth/logout', endpoint='auth_logout')

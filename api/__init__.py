from flask_restful import Api

from app import *

from .v1.errors import errors

api = Api(app, errors=errors)

# INFO: auth related API resources
from .v1.auth import AuthSignup, AuthLogin, AuthAccessToken, AuthCurrentUser

api.add_resource(AuthSignup, '/api/v1/auth/signup', endpoint='auth_login')
api.add_resource(AuthLogin, '/api/v1/auth/login', endpoint='auth_signup')
api.add_resource(AuthAccessToken, '/api/v1/auth/access-token', endpoint='auth_access_token')
api.add_resource(AuthCurrentUser, '/api/v1/auth/current-user', endpoint='auth_current_user')

# INFO: users related API resources
from .v1.users import UsersAll, UsersOne

api.add_resource(UsersAll, '/api/v1/users', endpoint='users_all')
api.add_resource(UsersOne, '/api/v1/users/<int:user_id>', endpoint='users_one')

# INFO: admin related API resources
from .v1.admin import AdminUsers, AdminUsersOne

api.add_resource(AdminUsers, '/api/v1/admin/users', endpoint='admin_users')
api.add_resource(AdminUsersOne, '/api/v1/admin/users/<int:user_id>', endpoint='admin_users_one')

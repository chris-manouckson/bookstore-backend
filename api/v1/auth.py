from flask_restful import Resource

from mocks.user import user_mock

class AuthSignup(Resource):
  def post(self):
    return {
      'data': {
        'user': user_mock,
        'token': 'token',
      },
      'message': 'User has been successfully signed up.',
    }

class AuthLogin(Resource):
  def get(self):
    # TODO: implement user login logic
    return {
      'data': {
        'token': 'token'
      },
      'message': 'User has been successfully logged in.',
    }

class AuthCurrent(Resource):
  def get(self):
    # TODO: implement current user getting logic
    return {
      'data': {
        'user': user_mock,
      },
      'message': '' ,
    }

class AuthLogout(Resource):
  def delete(self):
    # TODO: implement user logout logic
    return {
      'data': None,
      'message': 'User has been successfully logged out.',
    }, 201

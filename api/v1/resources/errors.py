from werkzeug.exceptions import HTTPException

class InternalServerError(HTTPException):
  pass

# INFO: auth related errors

class AuthUserAlreadyExistsError(HTTPException):
  pass

class AuthUserNotFoundError(HTTPException):
  pass

class AuthInvalidPasswordError(HTTPException):
  pass

class AuthUnauthorizedError(HTTPException):
  pass

def create_message_data(text=''):
  """Creates objects that fits response message format"""

  return {
    'text': text,
    'type': 'error',
  }

errors = {
  'InternalServerError': {
    'message': create_message_data('Something went wrong.'),
    'status': 500,
  },

  'AuthUserAlreadyExistsError': {
    'message': create_message_data('User with provided email or phone already exists.'),
    'status': 400,
  },
  'AuthUserNotFoundError': {
    'message': create_message_data('User with provided email not found.'),
    'status': 404,
  },
  'AuthInvalidPasswordError': {
    'message': create_message_data('Invalid password.'),
    'status': 400,
  },
  'AuthUnauthorizedError': {
    'message': create_message_data('Unauthorized.'),
    'status': 401,
  },
}

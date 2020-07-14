from werkzeug.exceptions import HTTPException

class InternalServerError(HTTPException):
  pass

class ForbiddenError(HTTPException):
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

class AuthAdminUserRoleRequiredError(HTTPException):
  pass

# INFO: users related errors

class UsersByIdNotFoundError(HTTPException):
  pass

class UsersUserAlreadyExistsError(HTTPException):
  pass

# INFO: user roles related errors

class UserRolesByIdNotFoundError(HTTPException):
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
  'ForbiddenError': {
    'message': create_message_data('Permession denied.'),
    'status': 403,
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
  'AuthAdminUserRoleRequiredError': {
    'message': create_message_data('Admin user role required.'),
    'status': 403,
  },

  'UsersByIdNotFoundError': {
    'message': create_message_data('User with provided id not found.'),
    'status': 404,
  },
  'UsersUserAlreadyExistsError': {
    'message': create_message_data('User with provided email or phone already exists.'),
    'status': 400,
  },

  'UserRolesByIdNotFoundError': {
    'message': create_message_data('User role with provided id not found.'),
    'status': 404,
  },
}

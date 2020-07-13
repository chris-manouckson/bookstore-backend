from flask_jwt_extended import jwt_required, get_jwt_identity

from models import User
from .errors import AuthUserNotFoundError, AuthAdminUserRoleRequiredError

def admin_user_role_required(request_handle_function):
  @jwt_required
  def wrapper(*args, **kwargs):
    current_user_id = get_jwt_identity()

    current_user = User.query.get(current_user_id)

    if not current_user:
      raise AuthUserNotFoundError
    
    if not current_user.role.title == 'admin':
      raise AuthAdminUserRoleRequiredError

    return request_handle_function(*args, **kwargs)
  
  return wrapper

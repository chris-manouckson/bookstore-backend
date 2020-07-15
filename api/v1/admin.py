from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from db import *
from jwt_manager import *
from models import User, UserRole
from .admin_user_role_required import *

from .errors import (
  UsersByIdNotFoundError,
  UserRolesByIdNotFoundError,
  UsersByIdNotFoundError,  
  ForbiddenError,
)

class AdminUsers(Resource):
  @admin_user_role_required
  def post(self):
    request_data = request.get_json()

    if 'first_name' in request_data:
      first_name = request_data['first_name']
    if 'last_name' in request_data:
      last_name = request_data['last_name']
    if 'email' in request_data:
      email = request_data['email']
    if 'phone' in request_data:
      phone = request_data['phone']
    if 'password' in request_data:
      password = request_data['password']
    if 'role_id' in request_data:
      role_id = request_data['role_id']
    
    user_role = UserRole.query.get(role_id)

    if not user_role:
      raise UserRolesByIdNotFound

    if User.query.filter_by(email=email).first() or User.query.filter_by(phone=phone).first():
      raise UsersUserAlreadyExistsError

    new_user = User(
      first_name,
      last_name,
      email,
      phone,
      password,
      user_role.id,
    )

    db.session.add(new_user)
    db.session.commit()

    response_data = {
      'user': new_user.get_data(),
    }
    response_message = {
      'text': 'New user with role {} has been successfully created.'.format(user_role.title),
      'type': 'success',
    }

    return jsonify(data=response_data, message=response_message, status=200)

class AdminUsersOne(Resource):
  @admin_user_role_required
  def delete(self, user_id):
    current_user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if not user:
      raise UsersByIdNotFoundError

    db.session.delete(user)
    db.session.commit()

    response_message = {
      'text': 'Your account was successfully deleted.',
      'type': 'success',
    }

    return jsonify(message=response_message, status=201)

class AdminUserRoles(Resource):
  @admin_user_role_required
  def get(self):
    user_roles = UserRole.query.all()

    response_data = {
      'user_roles': [user_role.get_data() for user_role in user_roles],
    }

    return jsonify(data=response_data, status=200)

class AdminUserRolesOne(Resource):
  @admin_user_role_required
  def get(self, user_role_id):
    user_role = UserRole.query.get(user_role_id)

    response_data = {
      'user_role': user_role.get_data(),
    }

    return jsonify(data=response_data, status=200)

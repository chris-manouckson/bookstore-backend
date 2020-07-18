from flask import request, jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from db import *
from jwt_manager import *
from models import UserRole, User, bcrypt
from .admin_user_role_required import *
from .parse_pagination_query import *

from mocks.user import user_mock
from mocks.token import token_mock

from .errors import (
  UsersByIdNotFoundError,
  UserRolesByIdNotFoundError,
  ForbiddenError,
)

class UsersAll(Resource):
  @parse_pagination_query
  def get(self, offset, limit):
    author_user_role = UserRole.query.filter_by(title='author').first()

    users_query = User.query.filter_by(role_id=author_user_role.id)

    users_total = users_query.count()

    users = users_query.offset(offset).limit(limit)

    response_data = {
      'users': [user.get_data() for user in users],
      'pagination': {
        'offset': offset,
        'limit': limit,
        'total': users_total,
      },
    }

    return jsonify(data=response_data, status=200)

  @jwt_required
  def delete(self):
    current_user_id = get_jwt_identity()

    user = User.query.get(current_user_id)

    db.session.delete(user)
    db.session.commit()

    response_message = {
      'text': 'Your account was successfully deleted.',
      'type': 'success',
    }

    return jsonify(message=response_message, status=201)

class UsersOne(Resource):
  def get(self, user_id):
    user = User.query.get(user_id)

    if not user:
      raise UsersByIdNotFoundError

    response_data = {
      'user': user.get_data(),
    }

    return jsonify(data=response_data, status=200)
  
  @jwt_required
  def put(self, user_id):
    current_user_id = get_jwt_identity()

    if current_user_id != user_id:
      raise ForbiddenError

    user = User.query.get(user_id)

    if not user:
      raise UsersByIdNotFoundError

    request_data = request.get_json()

    if 'first_name' in request_data:
      user.first_name = request_data['first_name']
    if 'last_name' in request_data:
      user.last_name = request_data['last_name']
    if 'phone' in request_data:
      user.phone = request_data['phone']

    response_data = {
      'user': user.get_data(),
    }
    response_message = {
      'text': 'Your account was successfully deleted.',
      'type': 'success',
    }

    return jsonify(data=response_data, message=response_message, status=200)

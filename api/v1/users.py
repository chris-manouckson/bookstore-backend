from flask import request, jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import asc, desc

from db import *
from jwt_manager import *
from models import User, bcrypt
from .admin_user_role_required import *
from .parse_pagination_query import *
from .parse_order_query import *
from .parse_search_query import *

from mocks.user import user_mock
from mocks.token import token_mock

from .errors import (
  UsersByIdNotFoundError,
  ForbiddenError,
)

class UsersAll(Resource):
  @parse_pagination_query
  @parse_order_query
  @parse_search_query
  def get(self, offset, limit, order=('id', 'asc'), search=''):
    users_query = User.query

    if search:
      search_regex = '%{}%'.format(search)

      users_query = users_query.filter(
        User.first_name.ilike(search_regex)
        | User.last_name.ilike(search_regex)
        | User.email.ilike(search_regex)
      )

    user_column_names = User.get_column_names()

    order_column_name, order_direction = order

    if order_column_name in user_column_names:
      if order_direction == 'desc':
        users_query = users_query.order_by(desc(order_column_name))
      else:
        users_query = users_query.order_by(order_column_name)

    users_total = users_query.count()

    users = users_query.offset(offset).limit(limit)

    response_data = {
      'users': [user.get_data() for user in users],
      'pagination': {
        'offset': offset,
        'limit': limit,
        'total': users_total,
      },
      'order': {
        'column_name': order_column_name,
        'direction': order_direction,
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
    
    db.session.commit()

    response_data = {
      'user': user.get_data(),
    }
    response_message = {
      'text': 'Your account was successfully deleted.',
      'type': 'success',
    }

    return jsonify(data=response_data, message=response_message, status=200)

from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import (
  jwt_required, create_access_token,
  jwt_refresh_token_required, create_refresh_token,
  get_jwt_identity
)

from db import *
from jwt_manager import *
from models import UserRole, User, bcrypt

from mocks.user import user_mock
from mocks.token import token_mock

from .errors import (
  AuthUserAlreadyExistsError,
  AuthUserNotFoundError,
  AuthInvalidPasswordError,
)

class AuthSignup(Resource):
  def post(self):
    request_data = request.get_json()

    first_name = request_data['first_name']
    last_name = request_data['last_name']
    email = request_data['email']
    phone = request_data['phone']
    password = request_data['password']

    if User.query.filter_by(email=email).first() or User.query.filter_by(phone=phone).first():
      raise AuthUserAlreadyExistsError

    author_user_role = UserRole.query.filter_by(title='author').first()

    new_user = User(
      first_name,
      last_name,
      email,
      phone,
      password,
      author_user_role.id,
    )

    db.session.add(new_user)
    db.session.commit()

    response_data = {
      'user': new_user.get_data(),
      # TODO: generate refresh token
      'refresh_token': token_mock,
    }
    response_message = {
      'text': 'Your author account has been successfully created.',
      'type': 'success',
    }

    return jsonify(data=response_data, message=response_message, status=200)

class AuthLogin(Resource):
  def post(self):
    pass
    request_data = request.get_json()

    email = request_data['email']
    password = request_data['password']

    user = User.query.filter_by(email=email).first()

    if not user:
      raise AuthUserNotFoundError
    
    if not bcrypt.check_password_hash(user.password, password):
      raise AuthInvalidPasswordError
    
    response_data = {
      'access_token': create_access_token(identity=user.id),
      'refresh_token': create_refresh_token(identity=user.id)
    }
    response_message = {
      'text': 'You have been successfully logged in as {}.'.format(user.get_data()['role']['title']),
      'type': 'success',
    }

    return jsonify(data=response_data, message=response_message, status=200)

class AuthAccessToken(Resource):
  @jwt_refresh_token_required
  def get(self):
    current_user_id = get_jwt_identity()

    user = User.query.get(current_user_id)

    if not user:
      raise AuthUserNotFoundError

    response_data = {
      'access_token': create_access_token(identity=user.id),
    }

    return jsonify(data=response_data, status=200)

class AuthCurrentUser(Resource):
  @jwt_required
  def get(self):
    current_user_id = get_jwt_identity()

    user = User.query.get(current_user_id)

    if not user:
      raise AuthUserNotFoundError

    response_data = {
      'user': user.get_data(),
    }

    return jsonify(data=response_data, status=200)

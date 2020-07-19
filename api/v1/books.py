from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import desc

from db import *
from jwt_manager import *
from models import User, Book
from .admin_user_role_required import *
from .parse_pagination_query import *
from .parse_order_query import *
from .parse_search_query import *

from constants import price_currencies

from mocks.book_isbn import book_isbn_mock

from .errors import (
  AuthUnauthorizedError,
  BooksByIdNotFoundError,
  ForbiddenError,
)

class BooksAll(Resource):
  @jwt_required
  def post(self):
    current_user_id = get_jwt_identity()

    current_user = User.query.get(current_user_id)

    if not current_user:
      raise AuthUnauthorizedError

    request_data = request.get_json()

    new_book_description = ''

    if 'description' in request_data:
      new_book_description = request_data['description']

    new_book_price_amount = 0
    new_book_price_currency = price_currencies['usd']

    if 'price' in request_data and isinstance(request_data['price'], dict):
      if 'amount' in request_data['price']:
        new_book_price_amount = request_data['price']['amount']

      if 'currency' in request_data['price']:
        new_book_price_currency = request_data['price']['currency']

    new_book = Book(
      title=request_data['title'],
      description=new_book_description,
      isbn=request_data['isbn'],
      price_amount=new_book_price_amount,
      price_currency=new_book_price_currency,
    )

    author_ids = [current_user_id]

    if 'author_ids' in request_data and type(request_data['author_ids']) == list:
      author_ids = list(set(author_ids + request_data['author_ids']))

    for author_id in list(set(author_ids)):
      author = User.query.get(author_id)
      if author:
        author.books.append(new_book)

    db.session.add(new_book)
    db.session.commit()

    response_data = {
      'book': new_book.get_data(),
    }
    response_message = {
      'text': 'Your book has been successfully created',
      'type': 'success',
    }
    
    return jsonify(data=response_data, message=response_message, status=200)

  @parse_pagination_query
  @parse_order_query
  @parse_search_query
  def get(self, offset, limit, order=('id', 'asc'), search=''):
    books_query = Book.query

    if search:
      search_regex = '%{}%'.format(search)

      books_query = books_query.filter(
        Book.title.ilike(search_regex)
        | Book.description.ilike(search_regex)
        | Book.isbn.ilike(search_regex)
      )

    order_column_name, order_direction = order

    book_column_names = Book.get_column_names()

    if order_column_name in book_column_names:
      if order_direction == 'desc':
        books_query = books_query.order_by(desc(order_column_name))
      else:
        books_query = books_query.order_by(order_column_name)

    books_total = books_query.count()

    books = Book.query.offset(offset).limit(limit)

    response_data = {
      'books': [book.get_data() for book in books],
      'pagination': {
        'offset': offset,
        'limit': limit,
        'total': books_total,
      },
      'order': {
        'column_name': order_column_name,
        'direction': order_direction,
      },
    }

    return jsonify(data=response_data, status=200)

class BooksOwn(Resource):
  @jwt_required
  def get(self):
    current_user_id = get_jwt_identity()

    current_user = User.query.get(current_user_id)

    response_data = {
      'books': [book.get_data() for book in current_user.books],
    }
    
    return jsonify(data=response_data, status=200)

class BooksOne(Resource):
  def get(self, book_id):
    book = Book.query.get(book_id)

    if not book:
      raise BooksByIdNotFoundError

    response_data = {
      'book': book.get_data(),
    }
    
    return jsonify(data=response_data, status=200)
  
  @jwt_required
  def put(self, book_id):
    current_user_id = get_jwt_identity()
    
    current_user = User.query.get(current_user_id)

    book = Book.query.get(book_id)

    if not book:
      raise BooksByIdNotFoundError
    
    if book not in current_user.books:
      raise ForbiddenError

    request_data = request.get_json()

    if 'title' in request_data:
      book.title = request_data['title']
    if 'description' in request_data:
      book.description = request_data['description']
    if 'isbn' in request_data:
      book.isbn = request_data['isbn']

    if 'price' in request_data and isinstance(request_data['price'], dict):
      if 'amount' in request_data['price']:
        book.price_amount = request_data['price']['amount']

      if 'currency' in request_data['price']:
        book.price_currency = request_data['price']['currency']
    
    db.session.commit()

    response_data = {
      'book': book.get_data(),
    }
    response_message = {
      'text': 'Your book has been successfully updated.',
      'type': 'success',
    }

    return jsonify(data=response_data, message=response_message, status=200)
  
  @jwt_required
  def delete(self, book_id):
    current_user_id = get_jwt_identity()
    
    current_user = User.query.get(current_user_id)

    book = Book.query.get(book_id)

    if not book:
      raise BooksByIdNotFoundError
    
    if book not in current_user.books and current_user.role.title != 'admin':
      raise ForbiddenError
    
    db.session.delete(book)
    db.session.commit()

    response_message = {
      'text': 'Your book has been successfully deleted.',
      'type': 'success',
    }

    return jsonify(message=response_message, status=201)

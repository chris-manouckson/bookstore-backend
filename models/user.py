from os import environ
import datetime

from flask_bcrypt import Bcrypt

from db import *

# INFO: users-books many to many relationship
users_books = db.Table(
  'users_books',
  db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
  db.Column('book_id', db.Integer, db.ForeignKey('books.id'), primary_key=True)
)

bcrypt = Bcrypt()

class User(db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(), nullable=False)
  last_name = db.Column(db.String(), nullable=False)
  email = db.Column(db.String(), unique=True, nullable=False)
  phone = db.Column(db.String(), unique=True, nullable=False)
  password = db.Column(db.String(), nullable=False)

  role_id = db.Column(
    db.Integer,
    db.ForeignKey('user_roles.id'),
    # TODO: select the author user role and pass as default value
    nullable=False
  )

  books = db.relationship(
    'Book',
    secondary=users_books,
    backref=db.backref('authors', lazy=True),
    lazy='subquery'
  )

  created_at = db.Column(db.DateTime(), server_default=db.func.now())
  updated_at = db.Column(db.DateTime(), server_default=db.func.now(), server_onupdate=db.func.now())

  def __init__(self, first_name, last_name, email, phone, password, role_id):
    self.first_name = first_name
    self.last_name = last_name
    self.email = email
    self.phone = phone
    self.password = bcrypt.generate_password_hash(password).decode()
    self.role_id = role_id

  def __repr__(self):
    return '<id {}>'.format(self.id)

  def get_data(self):
    return {
      'id': self.id,
      'first_name': self.first_name,
      'last_name': self.last_name,
      'email': self.email,
      'phone': self.phone,
      'role': {
        'title': self.role.title,
        'description': self.role.description,
      },
    }
  
  @staticmethod
  def get_column_names():
    return [str(column).split('.')[1] for column in User.__table__.columns]

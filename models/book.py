from db import *
from constants import price_currencies

class Book(db.Model):
  __tablename__ = 'books'

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(), nullable=False)
  description = db.Column(db.Text(), default='')
  isbn = db.Column(db.String(), nullable=False)
  price_amount = db.Column(db.Float(), default=0)
  price_currency = db.Column(db.String(), default=price_currencies['usd'])

  created_at = db.Column(db.DateTime(), server_default=db.func.now())
  updated_at = db.Column(db.DateTime(), server_default=db.func.now(), server_onupdate=db.func.now())

  def __init__(self, title, description, isbn, price_amount, price_currency):
    self.title = title
    self.description = description
    self.isbn = isbn
    self.price_amount = price_amount
    self.price_currency = price_currency
  
  def __repr__(self):
    return '<id {}>'.format(self.id)
  
  def get_data(self):
    return {
      'id': self.id,
      'title': self.title,
      'description': self.description,
      'isbn': self.isbn,
      'price': {
        'amount': self.price_amount,
        'currency': self.price_currency,
      },
      'authors': [author.get_data() for author in self.authors],
    }
  
  @staticmethod
  def get_column_names():
    return [str(column).split('.')[1] for column in Book.__table__.columns]

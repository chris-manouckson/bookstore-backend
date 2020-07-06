from db import *
from constants import price_currencies

class Book(db.Model):
  __tablename__ = 'books'

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(), nullable=False)
  description = db.Column(db.Text(), default='')
  isbn = db.Column(db.Integer, nullable=False)
  price_ammount = db.Column(db.Float(), default=0)
  price_currency = db.Column(db.String(), default=price_currencies['usd'])

  created_at = db.Column(db.DateTime(), server_default=db.func.now())
  updated_at = db.Column(db.DateTime(), server_default=db.func.now(), server_onupdate=db.func.now())

  def __init__(self, title, description, isbn, price_ammount, price_currency):
    self.title = title
    self.description = description
    self.isbn = isbn
    self.price_ammount = price_ammount
    self.price_currency = price_currency
  
  def __repr__(self):
    return '<id {}>'.format(self.id)

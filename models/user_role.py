from db import *

class UserRole(db.Model):
  __tablename__ = 'user_roles'

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(), unique=True, nullable=False)
  description = db.Column(db.Text())

  users = db.relationship('User', backref='role', lazy=True)

  def __init__(self, title, description):
    self.title = title
    self.description = description

  def __repr__(self):
    return '<id {}>'.format(self.id)

  def get_data(self):
    return {
      'id': self.id,
      'title': self.title,
      'description': self.description,
    }

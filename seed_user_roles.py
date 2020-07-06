#!venv/bin/python
from models import *

if __name__ == '__main__':
  db.session.add(UserRole(title='admin', description='can create, delete both users and books.'))
  db.session.add(UserRole(title='author', description='can create books and edit or delete them.'))
  db.session.commit()

#!venv/bin/python
from models import *

if __name__ == '__main__':
  admin_user_role = UserRole.query.filter_by(title='admin').first();

  db.session.add(
    User(
      first_name='Admin',
      last_name='Admin',
      email='admin@bookstore.com',
      phone='+1 11 11 11 11',
      password='12345678',
      role_id=admin_user_role.id,
    )
  )
  db.session.commit()

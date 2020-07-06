#!venv/bin/python
from os import environ

from flask_script import Manager, Command
from flask_migrate import Migrate, MigrateCommand

from app import *
from db import *
from models import *

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
  manager.run()

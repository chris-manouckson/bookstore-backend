#!venv/bin/python
from os import environ

from flask import Flask

app = Flask(__name__)

if __name__ == '__main__':
  flask_env = environ.get('FLASK_ENV')

  if flask_env == 'development':
    app.config.from_object('config.DevelopmentConfig')
  elif flask_env == 'production':
    app.config.from_object('config.ProductionConfig')
  else:
    app.config.from_object('config.Config')

  app.run()

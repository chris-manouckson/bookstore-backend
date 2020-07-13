from os import environ

from flask import Flask

app = Flask(__name__)

flask_env = environ.get('FLASK_ENV')

if flask_env == 'production':
  app.config.from_object('config.ProductionConfig')
else:
  app.config.from_object('config.DevelopmentConfig')

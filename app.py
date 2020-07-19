from os import environ

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

flask_env = environ.get('FLASK_ENV')

if flask_env == 'production':
  app.config.from_object('config.ProductionConfig')
else:
  app.config.from_object('config.DevelopmentConfig')

from os import environ, path

from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
  """Base config"""

  JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY')

class DevelopmentConfig(Config):
  DEBUG = True
  TESTING = True

  SERVER_NAME = '127.0.0.1:' + environ.get('PORT')

  SQLALCHEMY_DATABASE_URI = environ.get('DEVELOPMENT_DATABASE_URI')
  SQLALCHEMY_TRACK_MODIFICATIONS = True

class ProductionConfig(Config):
  DEBUG = False
  TESTING = False

  SQLALCHEMY_DATABASE_URI = environ.get('PRODUCTION_DATABASE_URI')
  SQLALCHEMY_TRACK_MODIFICATIONS = False

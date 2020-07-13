from flask_jwt_extended import JWTManager

from app import *

jwt_manager = JWTManager(app)

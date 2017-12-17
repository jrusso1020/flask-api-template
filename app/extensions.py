# Flask-SQLAlchemy extension instance
from flask_sqlalchemy import SQLAlchemy
# flask_marshmallow extension instance
from flask_marshmallow import Marshmallow
# Bcrypt
from flask_bcrypt import Bcrypt
# flask_restful
from flask_restful import Api
# celery
from celery import Celery

celery = Celery()

db = SQLAlchemy()

ma = Marshmallow()

bcrypt = Bcrypt()

api = Api()

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
from . import celeryconfig

celery = Celery(__name__, broker=celeryconfig.broker_url,
                backend=celeryconfig.result_backend,
                database_engine_options=celeryconfig.database_engine_options,
                broker_transport_options=celeryconfig.broker_transport_options,
                imports=celeryconfig.imports)

db = SQLAlchemy()

ma = Marshmallow()

bcrypt = Bcrypt()

api = Api()

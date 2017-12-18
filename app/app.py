import os

from flask import Flask, request, abort
from flask_cors import CORS
from . import config as Config
from .constants import INSTANCE_FOLDER_PATH

# from .api import
from .api import SignupAPI, LoginAPI, LogoutAPI
from .extensions import db, ma, bcrypt, api

# For import *
__all__ = ['create_app']

def create_app(config=None, app_name=None, blueprints=None):
  """Create a Flask app."""


  if app_name is None:
    app_name = Config.DefaultConfig.PROJECT


  app = Flask(app_name, instance_path=INSTANCE_FOLDER_PATH, instance_relative_config=True)
  configure_app(app, config)
  configure_hook(app)
  configure_endpoints(app)
  configure_extensions(app)
  configure_logging(app)
  cors = CORS(app, resources={r"/{}/*".format(app.config['API_ROOT']): {"origins": "*"}})


  if app.debug:
    print('running in debug mode')
  else:
    print('NOT running in debug mode')
  return app

def configure_app(app, config=None):
  """Different ways of configurations."""

  # http://flask.pocoo.org/docs/api/#configuration
  app.config.from_object(Config.DefaultConfig)

  if config:
    app.config.from_object(config)
    return

  mode = os.getenv('APPLICATION_MODE', 'LOCAL')

  print("Running in %s mode" % mode)

  app.config.from_object(Config.get_config(mode))


def configure_extensions(app):
  # flask-sqlalchemy
  db.init_app(app)

  # marshmallow
  ma.init_app(app)

  # bcrypt
  bcrypt.init_app(app)

def configure_endpoints(app):
  """Configure blueprints in views."""
  api.app = app
  api.add_resource(SignupAPI, "/{}/auth/signup".format(app.config['API_ROOT']), endpoint='signup')
  api.add_resource(LoginAPI, "/{}/auth/login".format(app.config['API_ROOT']), endpoint='login')
  api.add_resource(LogoutAPI, "/{}/auth/logout".format(app.config['API_ROOT']), endpoint='logout')


def configure_logging(app):
  """Configure file(info) and email(error) logging."""
  if app.debug or app.testing:
    # Skip debug and test mode. Just check standard output.
    return

  from logging import  INFO, DEBUG, ERROR, handlers, Formatter
  app.logger.setLevel(DEBUG)

  info_log = os.path.join(app.config['LOG_FOLDER'], 'info.log')
  info_file_handler = handlers.RotatingFileHandler(info_log, maxBytes=100000, backupCount=10)
  info_file_handler.setLevel(DEBUG)
  info_file_handler.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
  ))

  exception_log = os.path.join(app.config['LOG_FOLDER'], 'exception.log')
  exception_log_handler = handlers.RotatingFileHandler(exception_log, maxBytes=100000, backupCount=10)
  exception_log_handler.setLevel(ERROR)
  exception_log_handler.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
  ))
  app.logger.addHandler(info_file_handler)
  app.logger.addHandler(exception_log_handler)
  app.logger.info('hello log')

def configure_hook(app):
  @app.before_request
  def before_request():
    app.logger.debug('Hitting %s' % request.url)


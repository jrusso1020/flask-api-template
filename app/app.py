import os

from flask import Flask, make_response, jsonify, request
import simplejson as json
from . import config as Config
from .constants import INSTANCE_FOLDER_PATH

#import modesl for flask-admin
from .models import User

# from .api import
from .api import auth
from .extensions import db, csrf, ma, bcrypt
from . import response as Response

# For import *
__all__ = ['create_app']


DEFAULT_BLUEPRINTS = [
    auth
]

def create_app(config=None, app_name=None, blueprints=None):
  """Create a Flask app."""


  if app_name is None:
   app_name = Config.DefaultConfig.PROJECT
  if blueprints is None:
   blueprints = DEFAULT_BLUEPRINTS


  app = Flask(app_name, instance_path=INSTANCE_FOLDER_PATH, instance_relative_config=True)
  configure_app(app, config)
  configure_hook(app)
  configure_blueprints(app, blueprints)
  configure_extensions(app)
  configure_logging(app)
  configure_template_filters(app)
  configure_error_handlers(app)


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

  MODE = os.getenv('APPLICATION_MODE', 'LOCAL')

  print("Running in %s mode" % MODE)

  app.config.from_object(Config.get_config(MODE))


def configure_extensions(app):
  # flask-sqlalchemy
  db.init_app(app)

  # marshmallow
  ma.init_app(app)

  # bcrypt
  bcrypt.init_app(app)

  #flask-wtf
  #csrf.init_app(app)


def configure_blueprints(app, blueprints):
  """Configure blueprints in views."""

  for blueprint in blueprints:
    app.register_blueprint(blueprint)

def configure_template_filters(app):
  @app.template_filter('json')
  def jsonify(value):
    return json.dumps(value)



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
    '[in %(pathname)s:%(lineno)d]')
  )

  exception_log = os.path.join(app.config['LOG_FOLDER'], 'exception.log')
  exception_log_handler = handlers.RotatingFileHandler(exception_log, maxBytes=100000, backupCount=10)
  exception_log_handler.setLevel(ERROR)
  exception_log_handler.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s ')
  )
  app.logger.addHandler(info_file_handler)
  app.logger.addHandler(exception_log_handler)
  app.logger.info('hello log')

def configure_hook(app):
  @app.before_request
  def before_request():
    app.logger.debug('Hitting %s' % request.url)


def configure_error_handlers(app):
  @app.errorhandler(500)
  def server_error_page(error):
    return Response.make_error_resp(msg=str(error), code=500)

  @app.errorhandler(422)
  def semantic_error(error):
    return Response.make_error_resp(msg=str(error.description), code=422)

  @app.errorhandler(404)
  def page_not_found(error):
    return Response.make_error_resp(msg=str(error.description), code=404)

  @app.errorhandler(403)
  def page_forbidden(error):
    return Response.make_error_resp(msg=str(error.description), code=403)

  @app.errorhandler(400)
  def page_bad_request(error):
    # temp fix for csrf message
    if(error.description == "CSRF token missing or incorrect."):
       error.description = "You have lost connection. Please refresh the page."
    return Response.make_error_resp(msg=str(error.description), code=400)

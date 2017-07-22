import os
from .constants import INSTANCE_FOLDER_PATH
from .helpers import make_dir

class BaseConfig(object):
  PROJECT = "app" 


  # Get app root path, also can use flask.root_path.
  PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

  DEBUG = False
  USE_EMAIL = True
  TESTING = False
  PROD      = False

  SQLALCHEMY_TRACK_MODIFICATIONS = False

  BCRYPT_LOG_ROUNDS = 13

  #for session
  SECRET_KEY = os.environ['SECRET_KEY']
  API_ROOT = 'api'

  make_dir(INSTANCE_FOLDER_PATH)

  LOG_FOLDER = os.path.join(INSTANCE_FOLDER_PATH, 'logs')
  make_dir(LOG_FOLDER)

  # Fild upload, should override in production.
  # Limited the maximum allowed payload to 8 megabytes.
  # http://flask.pocoo.org/docs/patterns/fileuploads/#improving-uploads
  MAX_CONTENT_LENGTH = 8 * 1024 * 1024
  UPLOAD_FOLDER = os.path.join(INSTANCE_FOLDER_PATH, 'uploads')
  make_dir(UPLOAD_FOLDER)
   
   
class DefaultConfig(BaseConfig):
  SITE_NAME = "XXX"
  # Enable protection agains *Cross-site Request Forgery (CSRF)*
  WTF_CSRF_ENABLED = True

  # Define the database setting
  SQLALCHEMY_ECHO = False
  SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
  SQLALCHEMY_POOL_RECYCLE = 7200  
   
class LocalConfig(DefaultConfig):
  DEBUG = True
  USE_EMAIL = False
  DOMAIN_NAME = 'localhost:5000'
  SQLALCHEMY_ECHO = False
  PROD      = False
  BCRYPT_LOG_ROUNDS = 4
   
   
class TestConfig(BaseConfig):
  #Set Testing to False so we still have authentication when unit testing
  WTF_CSRF_ENABLED = False
  DOMAIN_NAME = 'localhost:5000'
  TESTING = False
  USE_EMAIL = False
  SQLALCHEMY_ECHO = False
  SQLALCHEMY_DATABASE_URI = os.environ['TEST_DATABASE_URL']
  BCRYPT_LOG_ROUNDS = 4
   
class StagingConfig(DefaultConfig):
  DOMAIN_NAME = 'STAGING_DOMAIN'
  DEBUG = False
  USE_EMAIL = False
  PROD      = True
   
class ProdConfig(DefaultConfig):
  DOMAIN_NAME = 'XXX'
  DEBUG = False
  USE_EMAIL = True
  PROD      = True

  SQLALCHEMY_ECHO = False
  SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


def get_config(MODE):
  SWITCH = {
    'LOCAL'     : LocalConfig,
    'STAGING'   : StagingConfig,
    'PRODUCTION': ProdConfig
  }
  return SWITCH[MODE]

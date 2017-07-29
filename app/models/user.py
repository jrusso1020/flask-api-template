import jwt
import os

from ..helpers import get_current_time, get_current_time_plus
from ..extensions import db, ma, bcrypt
from ..constants import STRING_LEN, EMAIL_LEN, PW_STRING_LEN
from .. import config as Config

MODE = os.getenv('APPLICATION_MODE', 'LOCAL')

config = Config.get_config(MODE)

class User(db.Model):

  __tablename__ = "users"
  def __repr__(self):
    return '<User %r>' % (self.user_name)

  id            = db.Column(db.Integer, primary_key = True)
  first_name    = db.Column(db.String(STRING_LEN), nullable=False)
  last_name     = db.Column(db.String(STRING_LEN), nullable=False)
  username      = db.Column(db.String(STRING_LEN),  index = True, unique = True, nullable=False)
  email         = db.Column(db.String(EMAIL_LEN), unique = True, nullable=False)
  api_token_hash= db.Column(db.String(255), nullable=True)
  created_at    = db.Column(db.DateTime, nullable=False, default = get_current_time)
  updated_at    = db.Column(db.DateTime, nullable=False, default = get_current_time, onupdate=get_current_time)

  # ================================================================
  # User Password

  password = db.Column('password', db.String(PW_STRING_LEN), nullable= False)

  # Relationships

  

  def __init__(self, first_name, last_name, username, email, password):
    self.first_name = first_name
    self.last_name = last_name
    self.username = username
    self.email = email
    hashed_password = bcrypt.generate_password_hash(
            password, app.config['BCRYPT_LOG_ROUNDS']
        )
    self.password = hashed_password if type(hashed_password)==str else hashed_password.decode('utf-8')

  def encode_auth_token(self, user_id):
    try:
      payload = {
        'exp': get_current_time_plus(minutes=30),
        'iat': get_current_time(),
        'sub': user_id
      }
      token = jwt.encode(
          payload,
          app.config['SECRET_KEY'],
          algorithm='HS256'
        )
      user = User.by_id(user_id)
      hashed_token = bcrypt.generate_password_hash(
            token, app.config['BCRYPT_LOG_ROUNDS']
        )
      user.api_token_hash = hashed_token if type(hashed_token)==str else hashed_token.decode('utf-8')
      db.session.commit()
      return token
    except Exception as e:
      return e

  # ================================================================

  # ================================================================
  # methods


  # ================================================================
  # Class methods

  @classmethod
  def decode_auth_token(cls, auth_token):
    try:
      payload = jwt.decode(auth_token, config.SECRET_KEY)
      # check the hash of what we expect the token to be and token we got to be the same
      if bcrypt.check_password_hash(User.by_id(payload['sub']).api_token_hash, auth_token):
        return payload['sub']
      else:
        return 'Token does not match Api Token.'
    except jwt.ExpiredSignatureError:
      return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
      return 'Invalid Token. Please log in again.'

  @classmethod
  def is_username_taken(cls, username):
    return db.session.query(db.exists().where(User.username==username)).scalar()

  @classmethod
  def is_email_taken(cls, email):
    return db.session.query(db.exists().where(User.email==email)).scalar()

  @classmethod
  def by_id(cls, id):
    return cls.query.filter(User.id==id).first()

  @classmethod
  def by_username(cls, username):
    return User.query.filter(User.username == username).first()

class UserSchema(ma.Schema):
  class Meta:
    fields = ('id', 'username', 'email', 'first_name', 'last_name')

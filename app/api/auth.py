from flask_restful import Resource, reqparse
from ..extensions import db, bcrypt
from ..models import User
from ..decorators import authorize

class SignupAPI(Resource):
  def __init__(self):
    self.parser = reqparse.RequestParser()
    self.parser.add_argument('first_name', type=str, required=True, help='No first name provided', location='json')
    self.parser.add_argument('last_name', type=str, required=True, help='No last name provided', location='json')
    self.parser.add_argument('username', type=str, required=True, help='No username provided', location='json')
    self.parser.add_argument('email', type=str, required=True, help='No email provided', location='json')
    self.parser.add_argument('password', type=str, required=True, help='No password provided', location='json')
    super(SignupAPI, self).__init__()

  def get(self):
    pass

  def post(self):
    args = self.parser.parse_args()
    try:
      user = User(
        first_name=args['first_name'],
        last_name=args['last_name'],
        username=args['username'],
        email=args['email'],
        password=args['password']
      )
      db.session.add(user)
      db.session.commit()
      auth_token = user.encode_auth_token(user.id)
      return {'auth_token': auth_token.decode('utf-8')}, 201
    except Exception as e:
      return {'error': "{}".format(e)}, 500

class LoginAPI(Resource):
  def __init__(self):
    self.parser = reqparse.RequestParser()
    self.parser.add_argument('username', type=str, required=True, help='No username provided', location='json')
    self.parser.add_argument('password', type=str, required=True, help='No password provided', location='json')
    super(LoginAPI, self).__init__()

  def get(self):
    pass

  def post(self):
    args = self.parser.parse_args()
    try:
      user = User.by_username(args['username'])
      if user and bcrypt.check_password_hash(user.password, args['password']):
        auth_token = user.encode_auth_token(user.id)
        if auth_token:
          return {'auth_token': auth_token.decode('utf-8')}, 200
      else:
        return {'error': "User doesn't Exist!"}, 404
    except Exception as e:
      return {'error': "{}".format(e)}, 500

class LogoutAPI(Resource):
  decorators = [authorize]
  def __init__(self):
    super(LogoutAPI, self).__init__()

  def get(self):
    pass

  def post(self, user):
    try:
      return {'user': user.id}, 200
    except Exception as e:
      return {'error': "{}".format(e)}, 500

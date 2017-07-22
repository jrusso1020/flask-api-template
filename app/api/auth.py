from flask import Blueprint, request
from ..extensions import db, bcrypt
from ..models import User
from .. import response as Response
from ..decorators import authorize

auth = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth.route('/signup', methods=['POST'])
def signup():
  if not request.json:
    return Response.make_error_resp(msg='Must have Content-Type of application/json.', code=415)
  elif not set(['first_name', 'last_name', 'username', 'email', 'position', 'password', 'location_id', 'company_id']).issubset(set(request.json)):
    return Response.make_error_resp(msg='Missing information for signup!', code=409)
  elif User.is_username_taken(request.json['username']):
    return Response.make_error_resp(msg="This username is already taken!", code=409)
  elif User.is_email_taken(request.json['email']):
    return Response.make_error_resp(msg="This email is already taken!", code=409)

  try:
    user = User(
        first_name=request.json['first_name'],
        last_name=request.json['last_name'],
        username=request.json['username'],
        email=request.json['email'],
        password=request.json['password'],
      )
    db.session.add(user)
    db.session.commit()
    auth_token = user.encode_auth_token(user.id)
    return Response.make_auth_success_resp(auth_token.decode())
  except Exception as e:
    return Response.make_exception_resp(exception=e)

@auth.route('/login', methods=['POST'])
def login():
  if not request.json:
    return Response.make_error_resp(msg='Must have Content-Type of application/json.', code=415)
  elif 'username' not in request.json:
    return Response.make_error_resp(msg="You forgot the username!", code=409)
  elif 'password' not in request.json:
    return Response.make_error_resp(msg="You forgot the password!", code=409)

  try:
    user = User.by_username(request.json['username'])
    if user and bcrypt.check_password_hash(user.password, request.json['password']):
      auth_token = user.encode_auth_token(user.id)
      if auth_token:
        return Response.make_auth_success_resp(auth_token.decode(), msg='Login Successful!')
    else:
      return Response.make_error_resp(msg="User doesn't exist!", code=404)
  except Exception as e:
    return Response.make_error_resp(msg="Fail Try Again!", code=500)

@auth.route('/logout', methods=['POST'])
@authorize
def logout(user):
  try:
    return Response.make_success_resp(msg='Logout Successful')
  except Exception as e:
    return Response.make_error_resp(msg="Fail Try Again!", code=500)


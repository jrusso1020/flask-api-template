from functools import wraps
from flask import abort, request
from .models import User
import jwt

def authorize(f):
  @wraps(f)
  def decorated_function(*args, **kws):
    if not 'Authorization' in request.headers:
      abort(401)

    user = None
    auth_header = request.headers.get('Authorization')
    if auth_header:
      auth_token = auth_header
    else:
      auth_token = ''
    if auth_token:
      user_id = User.decode_auth_token(auth_token)
      print(user_id)
      if not isinstance(user_id, str):
        user = User.by_id(user_id)
      else:
        abort(401)

    return f(user, *args, **kws)
  return decorated_function

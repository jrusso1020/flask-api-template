import unittest

from . import AppTestCase, API_ROOT
from app.extensions import db
from app.models import User, Location, Company

class TestUserModel(AppTestCase):
  def test_encode_auth_token(self):
    user = User.by_username('jdoe')
    auth_token = user.encode_auth_token(user.id)
    self.assertTrue(isinstance(auth_token, bytes))

  def test_decode_auth_token(self):
    user = User.by_username('jdoe')
    auth_token = user.encode_auth_token(user.id)
    self.assertTrue(isinstance(auth_token, bytes))
    self.assertEqual(User.decode_auth_token(auth_token), user.id)

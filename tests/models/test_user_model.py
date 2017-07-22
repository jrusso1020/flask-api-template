import unittest

from . import AppTestCase, API_ROOT
from app.extensions import db
from app.models import User, UserSchema, Location, Company

class TestUserModel(AppTestCase):
  def test_encode_auth_token(self):
    location = Location.by_full_address('123 Test St', 'New York', 'New York', '10036')
    company = Company.by_name('Test Company')
    user = User(
      'John', 'Doe', 'jdoe', 'jdoe@gmail.com', 'Manager', 'test123', location.id, company.id
      )
    db.session.add(user)
    db.session.commit()
    auth_token = user.encode_auth_token(user.id)
    self.assertTrue(isinstance(auth_token, bytes))

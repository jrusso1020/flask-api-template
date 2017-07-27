import unittest
import json

from . import AppTestCase, API_ROOT
from app.models import User, Location, Company

class TestAuth(AppTestCase):
  def test_signup(self):
    user = User.by_username('jdoe')
    response = self.client.post(API_ROOT+'/auth/signup', data=json.dumps(dict(
      first_name='Tester',
        last_name='Tester',
        username='tester',
        email='tester@gmail.com',
        position='Bossman',
        password='tester',
        location_id=user.location_id,
        company_id=user.company_id)), content_type='application/json')
    data = json.loads(response.data.decode())
    self.assertTrue(data['success'])
    self.assertTrue(data['message']=='Successfully registered.')
    self.assertTrue(data['auth_token'])
    self.assertTrue(response.content_type=='application/json')
    self.assertEqual(response.status_code, 200)

  def test_login_logout(self):
    response, data = self.login('jdoe', 'test123')
    self.assertTrue(data['success'])
    self.assertTrue(data['message']=='Login Successful!')
    self.assertTrue(data['auth_token'])
    self.assertTrue(response.content_type=='application/json')
    self.assertEqual(response.status_code, 200)
    response = self.client.post(API_ROOT+'/auth/logout', headers=dict(Authorization=data['auth_token']))
    data = json.loads(response.data.decode())
    self.assertTrue(data['success'])
    self.assertTrue(data['message']=='Logout Successful')
    self.assertEqual(response.status_code, 200)

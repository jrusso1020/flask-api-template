from flask_testing import TestCase

from app import create_app
from app.extensions import db
from app.config import TestConfig
from app.models import Location, Company

API_ROOT = TestConfig.API_ROOT

class AppTestCase(TestCase):

  def create_app(self):
    """Create and return a testing flask app."""
    app = create_app(TestConfig)
    return app

  def init_data(self):
    #default data initilization
    location = Location(street_address='123 Test St', city='New York', state='New York', zipcode='10036')
    company = Company(name='Test Company', industry='Poultry', headquarter_location_id=location.id)
    db.session.add(location)
    db.session.add(company)
    db.session.commit()

  def setUp(self):
    """Reset all tables before testing."""
    db.create_all()
    self.init_data()

  def tearDown(self):
    """Clean db session and drop all tables."""
    db.drop_all()

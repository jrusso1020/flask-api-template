# Flask-SQLAlchemy extension instance
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# flask_marshmallow extension instance
from flask_marshmallow import Marshmallow
ma = Marshmallow()

# Bcrypt
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()


# Flask-WTF csrf protection
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect()

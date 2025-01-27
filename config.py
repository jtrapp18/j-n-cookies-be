import os
import binascii
import secrets
from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from dotenv import load_dotenv

load_dotenv()

# Setup to serve React build
app = Flask(__name__)
CORS(app, supports_credentials=True)

# CORS: Allow credentials and specific frontend URLs for both dev and prod
CORS(app, supports_credentials=True, origins=['https://jtrapp18.github.io/j-n-cookies-fe', 'http://127.0.0.1:5173'])

# Set secret key and session cookie settings
secret_key = secrets.token_urlsafe(24)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', secret_key)
app.config['SESSION_COOKIE_HTTPONLY'] = True

# Set cookie security settings based on environment
if os.getenv('FLASK_ENV') == 'production':
    app.config['SESSION_COOKIE_SECURE'] = True  # Secure cookies in production
else:
    app.config['SESSION_COOKIE_SECURE'] = False  # In dev, use non-secure cookies

app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Helps with cross-site requests
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_PUBLIC_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)
migrate = Migrate(app, db)
db.init_app(app)

bcrypt = Bcrypt(app)

api = Api(app)
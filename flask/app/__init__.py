import logging
import os
from datetime import timedelta

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mailman import Mail
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask application
app = Flask(__name__, static_folder="static")
CORS(app)

# Application Configuration

# Debug Mode
app.config["DEBUG"] = os.getenv("FLASK_DEBUG", True)

# JSON Encoding Configuration
app.config["JSON_AS_ASCII"] = False

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite://")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Secret Key Configuration
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "your_default_secret_key_here"
)

# Password Salt Configuration
app.config["SECURITY_PASSWORD_SALT"] = os.environ.get(
    "SECURITY_PASSWORD_SALT", "your_default_password_salt_here"
)

# Flask-Security Options
app.config["SECURITY_REGISTERABLE"] = True
app.config["SECURITY_CONFIRMABLE"] = True
app.config["SECURITY_CHANGEABLE"] = True
app.config["SECURITY_RECOVERABLE"] = True

# Email Configuration
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
mail = Mail(app)

# JWT Configuration
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "your_jwt_secret_key")
app.config["JWT_COOKIE_SECURE"] = not app.config[
    "DEBUG"
]  # Set to True in production with HTTPS
app.config["JWT_COOKIE_CSRF_PROTECT"] = True  # Enable CSRF protection
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
    hours=1
)  # Set the access token expiry
app.config["JWT_TOKEN_LOCATION"] = ["headers"]

# JWT Error Handlers
jwt = JWTManager(app)


@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )


@jwt.expired_token_loader
def expired_token_callback():
    return (
        jsonify({"description": "The token has expired.", "error": "token_expired"}),
        401,
    )


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify({"description": "The token is invalid.", "error": "invalid_token"}),
        401,
    )


# Logging Configuration
logging.basicConfig(
    level=logging.DEBUG if app.config["DEBUG"] else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
app.logger.setLevel(logging.DEBUG if app.config["DEBUG"] else logging.INFO)

# Database Initialization
db = SQLAlchemy()
db.init_app(app)

# Include views after app initialization
from app import views

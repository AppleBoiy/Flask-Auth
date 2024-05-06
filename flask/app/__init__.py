import os
import logging
from datetime import timedelta

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager


app = Flask(__name__, static_folder="static")
CORS(app)

# Configuration
app.config["DEBUG"] = os.getenv("FLASK_DEBUG", True)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "your_secret_key")
app.config["JSON_AS_ASCII"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite://")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# JWT Configuration
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "your_jwt_secret_key")
app.config["JWT_COOKIE_SECURE"] = not app.config[
    "DEBUG"
]  # Set to True in production with HTTPS
app.config["JWT_COOKIE_CSRF_PROTECT"] = True  # Set CSRF protection
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
db = SQLAlchemy(app)

# Include views after app initialization
from app import views

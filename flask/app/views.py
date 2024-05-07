import logging

from sqlalchemy.sql import text
from flask import request, jsonify
from flask_restx import Api, Resource, fields
from flask_login import LoginManager

from flask_cors import cross_origin
from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
    unset_jwt_cookies,
    jwt_required,
    get_jwt_identity,
)

from app import app, db
from app.models.user import User

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = "login"  # Specify the view for login
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # Load and return a user from the database based on the user_id
    return User.query.get(int(user_id))


api = Api(app)

login_model = api.model(
    "Login",
    {
        "username": fields.String(required=True, description="User name"),
        "password": fields.String(required=True, description="User password"),
    },
)


@api.route("/login")
class Login(Resource):
    @cross_origin(origin="*", headers=["Content-Type"])
    @api.expect(login_model, validate=True)
    def post(self):
        """
        API endpoint for user login.

        This API endpoint allows the user to login.

        Request Body:
        {
            "username": "string",
            "password": "string"
        }

        Responses:
        - If login is successful:
            {
                "login": true,
                "access_token": "string"
            }
            HTTP status code: 200

        - If login fails due to invalid credentials:
            {
                "login": false,
                "message": "Invalid username or password"
            }
            HTTP status code: 401

        - If login fails due to unverified email:
            {
                "message": "Email not verified"
            }
            HTTP status code: 401
        """

        data = request.get_json()
        username = data["username"]
        password = data["password"]
        user = User.query.filter_by(username=username).first()

        logging.debug("login: " + str(username))

        if user and user.verify_password(password):
            if user.is_verified:  # Check if email is verified
                access_token = create_access_token(identity=username)
                response = jsonify({"login": True})
                set_access_cookies(response, access_token)
                return jsonify(login=True, access_token=access_token), 200
            else:
                return jsonify({"message": "Email not verified"}), 401
        return jsonify({"login": False, "message": "Invalid username or password"}), 401


@api.route("/logout")
class Logout(Resource):
    @cross_origin(origin="*", headers=["Content-Type", "Authorization"])
    @jwt_required()
    def get(self):
        """
        API endpoint for user logout.

        This API endpoint allows the user to logout.

        Responses:
        - If logout is successful:
            {
                "message": "Logout successful"
            }
            HTTP status code: 200
        """

        response = jsonify({"message": "Logout successful"})
        unset_jwt_cookies(response)
        return response, 200


@api.route("/users")
class Users(Resource):
    def get(self):
        """
        API endpoint to retrieve all users.

        Returns:
        - List of users:
            [
                {
                    "id": 1,
                    "username": "user1",
                    "email": "user1@example.com",
                    "verified": False
                },
                ...
            ]
            HTTP status code: 200
        """

        users = User.query.all()
        user_list = [user.to_dict() for user in users]
        return user_list, 200

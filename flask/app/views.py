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
from app.models.user import User, RolesUsers, Role

api = Api(app)


@api.route("/roles_users")
class RolesUser(Resource):
    def get(self):
        res = RolesUsers.query.all()
        return [r.to_dict() for r in res], 200


@api.route("/users")
class Users(Resource):
    def get(self):
        users = User.query.all()
        user_list = [user.to_dict() for user in users]
        return user_list, 200


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


register_model = api.model(
    "Register",
    {
        "username": fields.String(required=True, description="User name"),
        "email": fields.String(required=True, description="User email"),
        "password": fields.String(required=True, description="User password"),
    },
)


@api.route("/register")
class Register(Resource):
    @cross_origin(origin="*", headers=["Content-Type"])
    @api.expect(register_model, validate=True)
    def post(self):
        data = request.get_json()
        username = data["username"]
        email = data["email"]
        password = data["password"]

        # Check if username or email already exists
        if (
            User.query.filter_by(username=username).first()
            or User.query.filter_by(email=email).first()
        ):
            return jsonify({"message": "Username or email already exists"}), 400

        # Create a new user
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Registration successful"}), 200


@api.route("/logout", methods=["POST"])
class Logout(Resource):
    @cross_origin(origin="*", headers=["Content-Type", "Authorization"])
    @jwt_required()
    def post(self):
        response = jsonify({"message": "Logout successful"})
        unset_jwt_cookies(response)
        return response, 200

role_model = api.model(
    "Role",
    {
        "name": fields.String(required=True, description="Role name"),
    },
)

@api.route("/roles")
class Roles(Resource):
    def get(self):
        roles = Role.query.all()
        role_list = [role.to_dict() for role in roles]
        return role_list, 200

    @cross_origin(origin="*", headers=["Content-Type"])
    @jwt_required()
    @api.expect(role_model, validate=True)
    def post(self):
        data = request.get_json()
        name = data["name"]

        # Check if role already exists
        if Role.query.filter_by(name=name).first():
            return jsonify({"message": "Role already exists"}), 400

        # Create a new role
        new_role = Role(name=name)
        db.session.add(new_role)
        db.session.commit()

        return jsonify({"message": "Role created successfully"}), 200
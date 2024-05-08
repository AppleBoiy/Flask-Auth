from flask import request
from flask_restx import Api, Resource, fields
from flask_security import RegisterForm
from flask_security import SQLAlchemySessionUserDatastore, Security
from flask_cors import cross_origin

from wtforms import StringField
from wtforms.validators import DataRequired

from app import app, db
from app.models.user import User, Role

api = Api(app)

user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
security = Security(app, user_datastore)


# Define your API routes
@api.route("/users")
class ViewUsers(Resource):
    @cross_origin()
    def get(self):
        users = User.query.all()
        user_list = [user.to_dict() for user in users]
        return user_list, 200


@api.route("/users/<int:user_id>")
class SearchUser(Resource):
    @cross_origin()
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            return user.to_dict(), 200
        else:
            return {"message": "User not found"}, 404


# Define the user model for the input data
user_edit_model = api.model(
    "UserEdit",
    {
        "first_name": fields.String(required=True),
        "last_name": fields.String(required=True),
    }
)


@api.route("/users/<int:user_id>/edit")
class EditUser(Resource):
    @api.expect(user_edit_model)
    def put(self, user_id):
        user = User.query.get(user_id)
        if user:
            data = request.json
            first_name = data.get("first_name")
            last_name = data.get("last_name")

            user.edit_infomation(first_name, last_name)
            db.session.commit()

            return {"message": "User information updated successfully"}, 200
        else:
            return {"message": "User not found"}, 404

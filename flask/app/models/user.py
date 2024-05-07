from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)
    _email_verified = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @property
    def is_verified(self):
        return self._email_verified

    def verified(self):
        self._email_verified = True
        db.session.commit()

    @password.setter
    def password(self, password):
        self._password_hash = generate_password_hash(password)

    def get_id(self):
        return str(self.id)

    def verify_password(self, password):
        return check_password_hash(self._password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "verified": self._email_verified,
        }

    def __repr__(self):
        return f"<User {self.username}>"

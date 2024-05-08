from app import db
from flask_security import UserMixin, RoleMixin
from sqlalchemy import Boolean, DateTime, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref


class Role(db.Model, RoleMixin):
    __tablename__ = "role"
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))

    def to_dict(self):
        return {"id": self.id, "name": self.name, "description": self.description}


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = Column(Integer(), primary_key=True)
    email = Column(String(255), unique=True)
    password = Column(String(255), nullable=False)

    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)

    active = Column(Boolean())
    fs_uniquifier = Column(String(255), unique=True, nullable=False)
    confirmed_at = Column(DateTime())

    roles = relationship(
        "Role", secondary="roles_users", backref=backref("user", lazy="dynamic")
    )

    def edit_infomation(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def to_dict(self):
        user_dict = {
            "id": self.id,
            "email": self.email,
            "confirmed_at": (
                self.confirmed_at.isoformat() if self.confirmed_at else None
            ),
        }
        return user_dict

class RolesUsers(db.Model):
    __tablename__ = "roles_users"
    id = Column(Integer(), primary_key=True)
    user_id = Column("user_id", Integer(), ForeignKey("user.id"))
    role_id = Column("role_id", Integer(), ForeignKey("role.id"))

    def to_dict(self):
        return {"id": self.id, "user_id": self.user_id, "role_id": self.role_id}


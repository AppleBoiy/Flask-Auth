from flask.cli import FlaskGroup
from werkzeug.security import generate_password_hash


from app import app, db
from app.models.user import User, Role, RolesUsers

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    # Create roles
    roles_data = [
        {"name": "admin", "description": "Administrator"},
        {"name": "user", "description": "Regular User"},
    ]
    roles = [Role(**data) for data in roles_data]
    db.session.bulk_save_objects(roles)
    db.session.commit()

    # Create users
    users_data = [
        {
            "email": "admin@example.com",
            "username": "admin",
            "password": "admin_password",
            "active": True
        },
        {
            "email": "user@example.com",
            "username": "user",
            "password": "user_password",
            "active": True
        },
    ]
    users = [User(**data) for data in users_data]
    db.session.bulk_save_objects(users)

    # Create roles_users records
    roles_users_data = [
        {"user_id": 1, "role_id": 1},  # admin user with admin role
        {"user_id": 2, "role_id": 2},  # user user with user role
    ]
    roles_users = [RolesUsers(**data) for data in roles_users_data]
    db.session.bulk_save_objects(roles_users)

    db.session.commit()


if __name__ == "__main__":
    cli()

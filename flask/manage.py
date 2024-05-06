from flask.cli import FlaskGroup
from werkzeug.security import generate_password_hash


from app import app, db
from app.models.user import User

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    users_data = [
        {"username": "string", "email": "string@example.com", "password": "string"},
        {"username": "user1", "email": "user1@example.com", "password": "password1"},
        {"username": "user2", "email": "user2@example.com", "password": "password2"},
    ]

    for user_data in users_data:
        user = User(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"],
            email_confirmed=False,
        )
        db.session.add(user)
    db.session.commit()


if __name__ == "__main__":
    cli()

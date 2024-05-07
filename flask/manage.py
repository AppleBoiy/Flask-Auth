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
    # Manually adding users
    user1 = User(
        username="string",
        email="string@example.com",
        password="string",
    )
    user1.verified()
    db.session.add(user1)

    user2 = User(
        username="user1",
        email="user1@example.com",
        password="password1",
    )
    db.session.add(user2)

    user3 = User(
        username="user2",
        email="user2@example.com",
        password="password2",
    )
    db.session.add(user3)

    db.session.commit()


if __name__ == "__main__":
    cli()

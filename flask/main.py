from app import app, db
from app.models.user import User, Role
from flask_security import SQLAlchemySessionUserDatastore, Security


user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
security = Security(app, user_datastore)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

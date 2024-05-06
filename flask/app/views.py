from sqlalchemy.sql import text

from app import app
from app import db


@app.route("/")
def home():
    return "Flask says 'Hello world!'"


@app.route("/crash")
def crash():
    return 1 / 0


@app.route("/db")
def db_connection():
    try:
        with db.engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return "<h1>db works.</h1>"
    except Exception as e:
        return "<h1>db is broken.</h1>" + str(e)

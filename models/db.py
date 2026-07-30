import sqlite3
from flask import current_app, g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE_PATH"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
        g.db.execute("PRAGMA journal_mode = WAL")  # melhora leitura/escrita concorrente
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app):
    with app.app_context():
        db = get_db()
        with open(app.config["SCHEMA_PATH"], "r", encoding="utf-8") as f:
            db.executescript(f.read())
        db.commit()


def register_db(app):
    app.teardown_appcontext(close_db)

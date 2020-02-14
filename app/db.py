# coding: utf-8
from flask_sqlalchemy import SQLAlchemy

DB = None


def init_db(app):
    global DB
    if not DB:
        DB = SQLAlchemy(app)

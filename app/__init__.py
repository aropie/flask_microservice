# coding: utf-8
from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    from . import db
    db.init_db(app)

    from app.apis import blueprint as api
    app.register_blueprint(api, url_prefix='/api/v1')

    return app

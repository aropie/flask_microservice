# coding: utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(test_config=False):
    # create and configure the app
    app = Flask(__name__)
    if test_config is None:
        app.config.from_object('app.config.DevelopmentConfig')
    else:
        app.config.from_object('app.config.TestingConfig')

    db.init_app(app)

    from app.apis import blueprint as api
    app.register_blueprint(api, url_prefix='/api/v1')

    return app

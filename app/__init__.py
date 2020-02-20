# coding: utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()


def create_app(test_config=False):
    # create and configure the app
    app = Flask(__name__)
    prod = os.getenv('FLASK_PRODUCTION', None)

    if test_config:
        app.config.from_object('app.config.TestingConfig')
    elif prod:
        app.config.from_object('app.config.ProductionConfig')
    else:
        app.config.from_object('app.config.DevelopmentConfig')

    db.init_app(app)

    from app.apis import blueprint as api
    app.register_blueprint(api, url_prefix='/api/v1')

    return app

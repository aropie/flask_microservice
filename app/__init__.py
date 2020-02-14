# coding: utf-8
from flask import Flask
import os

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py')
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    from . import db
    db.init_db(app)

    from . import auth, users
    app.register_blueprint(auth.bp)
    app.register_blueprint(users.bp)

    return app

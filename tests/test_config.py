#!/usr/bin/env python3
import os


def test_development_config(app):
    app.config.from_object('app.config.DevelopmentConfig')
    assert app.config['DEBUG']
    assert not app.config['TESTING']
    assert (app.config['SQLALCHEMY_DATABASE_URI'] ==
            'postgresql://postgres:@db/user_service')


def test_testing_config(app):
    app.config.from_object('app.config.TestingConfig')
    assert app.config['DEBUG']
    assert app.config['TESTING']
    assert not app.config['PRESERVE_CONTEXT_ON_EXCEPTION']
    assert (app.config['SQLALCHEMY_DATABASE_URI'] ==
            'postgresql://postgres:@db/user_service_test')


def test_production_config(app):
    app.config.from_object('app.config.ProductionConfig')
    assert not app.config['DEBUG']
    assert not app.config['TESTING']

    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT', 5432)
    db = os.getenv('DB_DATABASE')

    expected_uri = (f'postgresql://{user}:{password}'
                    f'@{host}:{port}/{db}')

    assert app.config['SQLALCHEMY_DATABASE_URI'] == expected_uri

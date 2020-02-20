import os


class BaseConfig:
    RESTX_MASK_SWAGGER = False
    PRODUCTION = os.getenv('PRODUCTION', False)


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_URI', 'postgresql://'
                                        'postgres:@db/user_service')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'dev'
    DEBUG = True
    TESTING = False


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_URI', 'postgresql://'
                                        'postgres:@db/user_service_test')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'testing'
    DEBUG = True
    TESTING = True


class ProductionConfig(BaseConfig):
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT', 5432)
    DB_DATABASE = os.getenv('DB_DATABASE')

    SQLALCHEMY_DATABASE_URI = os.getenv('DB_URI',
                                        f'postgresql://{DB_USER}:{DB_PASSWORD}'
                                        f'@{DB_HOST}:{DB_PORT}/{DB_DATABASE}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'asdasdkadjfads'
    DEBUG = False
    TESTING = False

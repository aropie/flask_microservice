import os

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT', 5432)
DB_DATABASE = os.getenv('DB_DATABASE')

SQLALCHEMY_DATABASE_URI = os.getenv('DB_URI',
                                    f'postgresql://{DB_USER}:{DB_PASSWORD}'
                                    f'@{DB_HOST}:{DB_PORT}/{DB_DATABASE}')
SQLALCHEMY_TRACK_MODIFICATIONS = False

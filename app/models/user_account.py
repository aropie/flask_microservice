# coding: utf-8
import enum
import datetime
import crypt

from flask import current_app
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

from app import db


class Gender(enum.Enum):
    M = 1,
    F = 2,
    O = 3,
    U = 4


class UserAccount(db.Model):
    __tablename__ = 'user_account'

    id = db.Column(db.Integer, primary_key=True)
    salt = db.Column(db.String(19), nullable=False)
    hashed_password = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(250), nullable=False)
    middle_name = db.Column(db.String(250))
    father_surname = db.Column(db.String(250), nullable=False)
    mother_surname = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.Enum(Gender), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    birth_date = db.Column(db.Date, nullable=False)
    joined_at = db.Column(db.DateTime, nullable=False,
                          default=datetime.datetime.utcnow())
    cellphone = db.Column(db.String(10), nullable=False)

    def hash_password(self, password):
        self.salt = crypt.mksalt()
        salted_password = password + self.salt
        self.hashed_password = generate_password_hash(salted_password,
                                                      salt_length=16)

    def verify_password(self, password):
        salted_password = password + self.salt
        return check_password_hash(self.hashed_password, salted_password)

    def generate_auth_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        print(token)
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = UserAccount.query.get(data['id'])
        return user

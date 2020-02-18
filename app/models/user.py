# coding: utf-8
import enum
import datetime
import crypt

from flask import current_app
from werkzeug.security import check_password_hash, generate_password_hash
from marshmallow import Schema, fields
from marshmallow_enum import EnumField
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

from app.db import DB


class Gender(enum.Enum):
    M = 1,
    F = 2,
    O = 3,
    U = 4


class UserAccount(DB.Model):
    __tablename__ = 'user_account'

    id = DB.Column(DB.Integer, primary_key=True)
    salt = DB.Column(DB.String(16), nullable=False)
    hashed_password = DB.Column(DB.String(94), nullable=False)
    first_name = DB.Column(DB.String(250), nullable=False)
    middle_name = DB.Column(DB.String(250), nullable=False)
    father_surname = DB.Column(DB.String(250), nullable=False)
    mother_surname = DB.Column(DB.String(250), nullable=False)
    gender = DB.Column(DB.Enum(Gender), nullable=False)
    email = DB.Column(DB.String(250), nullable=False, unique=True)
    birth_date = DB.Column(DB.Date, nullable=False)
    joined_at = DB.Column(DB.DateTime, nullable=False,
                          default=datetime.datetime.utcnow())
    cellphone = DB.Column(DB.String(10), nullable=False)

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
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = UserAccount.query.get(data['id'])
        return user


class UserAccountSchema(Schema):
    id = fields.Int()
    first_name = fields.Str()
    middle_name = fields.Str()
    father_surname = fields.Str()
    mother_surname = fields.Str()
    gender = EnumField(Gender)
    email = fields.Email()
    birth_date = fields.Date()
    joined_at = fields.DateTime()
    cellphone = fields.Str()

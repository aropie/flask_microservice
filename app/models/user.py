# coding: utf-8
import datetime
import crypt
from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import check_password_hash, generate_password_hash
from marshmallow import Schema, fields

from app.db import DB
from app.models import Credentials



class UserAccount(DB.Model):
    __tablename__ = 'user_account'

    id = DB.Column(DB.Integer, primary_key=True)
    first_name = DB.Column(DB.String(250), nullable=False)
    middle_name = DB.Column(DB.String(250), nullable=False)
    father_surname = DB.Column(DB.String(250), nullable=False)
    mother_surname = DB.Column(DB.String(250), nullable=False)
    # sex = DB.Column(DB.String(250), nullable=False, choices=['M', 'F', 'U', 'NB'])
    email = DB.Column(DB.String(250), nullable=False, unique=True)
    birth_date = DB.Column(DB.Date, nullable=False)
    joined_at = DB.Column(DB.DateTime, nullable=False,
                          default=datetime.datetime.utcnow())
    cellphone = DB.Column(DB.String(10), nullable=False)

    def save_password(self, password):
        salt = crypt.mksalt()
        salted_password = password + salt
        hashed_pwd = generate_password_hash(salted_password, salt_length=16)
        login_details = Credentials(email=self.email,
                                    hashed_password=hashed_pwd,
                                    salt=salt)
        DB.session.add(login_details)


class UserAccountSchema(Schema):
    id = fields.Int()
    first_name = fields.Str()
    middle_name = fields.Str()
    father_surname = fields.Str()
    mother_surname = fields.Str()
    # sex = DB.Column(DB.String(250), nullable=False, choices=['M', 'F', 'U', 'NB'])
    email = fields.Email()
    birth_date = fields.Date()
    joined_at = fields.DateTime()
    cellphone = fields.Str()

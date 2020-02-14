# coding: utf-8
import datetime
from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import check_password_hash
from marshmallow import Schema, fields
from app.db import DB


class Credentials(DB.Model):
    __tablename__ = 'credentials'

    email = DB.Column(DB.Integer, DB.ForeignKey('user_account.email'),
                      primary_key=True)
    salt = DB.Column(DB.String(16), nullable=False)
    hashed_password = DB.Column(DB.String(94), nullable=False)

    user = DB.relationship('UserAccount',
                           backref=DB.backref('credentials', lazy=True))

    def is_password_correct(self, password):
        salted_password = password + self.salt
        return check_password_hash(self.hashed_password, salted_password)

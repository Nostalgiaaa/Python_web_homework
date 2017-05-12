from . import db
from flask_login import UserMixin
from . import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from datetime import datetime
import bleach
from markdown import markdown
import json


class Students(UserMixin, db.Model):
    __tablename__ = 'Students'
    Id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(80))

    def __init__(self, Id, password, email):
        self.Id = Id
        self.password = password
        self.email = email

    def __repr__(self):
        return '<Student %r>' % self.Id

    @property
    def password(self):
        raise AttributeError('password is not a readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.Id


class Manager(UserMixin, db.Model):
    __tablename__ = 'manager'
    Id = db.Column(db.String, primary_key=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(80))
    power = db.Column(db.Integer)

    def __init__(self, managerId, password, email):
        self.Id = managerId
        self.password = password
        self.email = email

    def __repr__(self):
        return '<Student %r>' % self.Id

    @property
    def password(self):
        raise AttributeError('password is not a readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.Id


class Teacher(UserMixin, db.Model):
    __tablename__ = 'teacher'
    Id = db.Column(db.String, primary_key=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(80), unique=True)

    def __init__(self, Id, password, email):
        self.Id = Id
        self.password = password
        self.email = email

    def __repr__(self):
        return '<Student %r>' % self.Id

    @property
    def password(self):
        raise AttributeError('password is not a readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    if Manager.query.get(int(user_id)):
        return Manager.query.get(int(user_id))
    elif Students.query.get(int(user_id)):
        return Students.query.get(int(user_id))
    elif Teacher.query.get(int(user_id)):
        return Teacher.query.get(int(user_id))









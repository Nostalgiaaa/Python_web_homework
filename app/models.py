from . import db
from flask_login import UserMixin
from . import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from datetime import datetime
import bleach
from markdown import markdown


class Students(UserMixin, db.Model):
    __tablename__ = 'Students'
    studentId = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(80), unique=True)

    def __init__(self, student_id, password, email):
        self.studentId = student_id
        self.password = password
        self.email = email

    def __repr__(self):
        return '<Student %r>' % self.studentId

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
    return Students.query.get(int(user_id))


class Manager(UserMixin, db.Model):
    __tablename__ = 'manager'
    managerId = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(80), unique=True)
    power = db.Column(db.Integer)

    def __init__(self, student_id, password, email):
        self.managerId = student_id
        self.password = password
        self.email = email

    def __repr__(self):
        return '<Student %r>' % self.studentId

    @property
    def password(self):
        raise AttributeError('password is not a readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Teacher(UserMixin, db.Model):
    __tablename__ = 'teacher'
    teacherId = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(80), unique=True)

    def __init__(self, student_id, password, email):
        self.teacherId = student_id
        self.password = password
        self.email = email

    def __repr__(self):
        return '<Student %r>' % self.studentId

    @property
    def password(self):
        raise AttributeError('password is not a readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)








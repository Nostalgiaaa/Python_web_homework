#coding:utf-8
from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField
from wtforms.validators import Required, ValidationError, InputRequired, Email
from ..models import *
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ..models import Students

def my_length_check(form, field):
    if len(field.data) < 6:
        raise ValidationError(u'密码长度大于等于六位')
    if len(field.data) >= 15:
        raise ValidationError(u'密码长度小于十五位')

def usercheck(form, field):
    if len(field.data) < 5:
        raise ValidationError(u'账户长度大于四位')
    if len(field.data) >= 15:
        raise ValidationError(u'账户长度小于十五位')


def commentcheck(form, field):
    if len(field.data) <= 8:
        raise ValidationError(u'回复内容长度大于8')
    if len(field.data) >= 15:
        raise ValidationError(u'回复内容长度小于150')

def gradecheck(form, field):
    try:
        int(field.data)
    except Exception as e:
        raise ValidationError(u'请填写数字，例如13届就填写13')
    if int(field.data) not in xrange(0, 30):
        raise ValidationError(u'请填写正确的届数，例如13')


def typecheck(form, field):
    try:
        int(field.data)
    except Exception as e:
        raise ValidationError(u'请填写数字，例如软件工程就填写2001')
    if len(field.data) != 4:
        raise ValidationError(u'长度为四位')


def classcheck(form, field):
    try:
        int(field.data)
    except Exception as e:
        raise ValidationError(u'请填写数字，例如4班就就填写04')
    if len(field.data) != 2:
        raise ValidationError(u'长度为两位')


def studentcheck(form, field):
    try:
        int(field.data)
    except Exception as e:
        raise ValidationError(u'请填写数字，例如30人就就填写30')
    if len(field.data) != 2:
        raise ValidationError(u'长度为两位')
    if int(field.data) not in xrange(1, 99):
        raise ValidationError(u'请填写数字，例如30人就就填写30')

def studentnumcheck(form, field):
    try:
        int(field.data)
    except Exception as e:
        raise ValidationError(u'请填写数字')
    if len(field.data) != 10:
        raise ValidationError(u'长度为十位')
    if not Students.query.filter_by(Id=field.data).first():
        raise ValidationError(u'学号不存在')



class NameForm(Form):
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
    name = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores'), validate_username, usercheck])
    password = PasswordField('what is your Password?', validators=[
        Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[InputRequired()])
    nickname = StringField('what is your nickname?', validators=[InputRequired()])
    mail = StringField('what is your real mail?', validators=[Email(), validate_email])
    submit = SubmitField(u'注册')


class LoginForm(Form):
    name = StringField('username?', validators=[InputRequired(), usercheck])
    password = PasswordField('password?', validators=[InputRequired(), my_length_check])
    type = SelectField(u'选择您的账号类型', choices=[(u'学生', u'学生'), (u'教师', u'教师'), (u'管理员', u'管理员')])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登录')


class RegStudent(Form):
    grade = StringField(u'年级', validators=[InputRequired(), gradecheck])
    typenum = StringField(u'院系专业', validators=[InputRequired(), typecheck])
    classnum = StringField(u'班级', validators=[InputRequired(), classcheck])
    studentnum = StringField(u'班级人数', validators=[InputRequired(), studentcheck])
    submit = SubmitField(u'确认添加班级')


class RegStudent_one(Form):
    grade = StringField(u'年级', validators=[InputRequired(), gradecheck])
    typenum = StringField(u'院系专业', validators=[InputRequired(), typecheck])
    classnum = StringField(u'班级', validators=[InputRequired(), classcheck])
    studentnum = StringField(u'学号', validators=[InputRequired(), studentcheck])
    submit_one = SubmitField(u'确认添加个人')


class RegStudent_password(Form):
    studentnum = StringField(u'学号', validators=[InputRequired(), studentnumcheck])
    submit_password = SubmitField(u'确认添加个人')

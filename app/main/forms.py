#coding:utf-8
from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import Required, ValidationError, InputRequired, Email
from ..models import *
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField


def my_length_check(form, field):
    if len(field.data) <= 6:
        raise ValidationError(u'密码长度大于六位')
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
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登录')


class PostForm(Form):
    title = StringField(u'标题?', validators=[InputRequired()])
    category = StringField(u'类别?', validators=[InputRequired()])
    body = PageDownField("What's on your mind?", validators=[InputRequired()])
    submit = SubmitField('Submit')


class CommentForm(Form):
    body = StringField('', validators=[InputRequired(), commentcheck])
    submit = SubmitField(u'提交')

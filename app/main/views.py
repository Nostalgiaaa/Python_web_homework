#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import main
from datetime import datetime
from flask import render_template, session, redirect, url_for, request, flash, current_app
from . import main
from .forms import NameForm, LoginForm, PostForm, CommentForm
from ..__init__ import db
from ..models import *
from flask_login import login_user
from flask_login import logout_user, login_required
from flask_login import current_user


@main.route('/login', methods=['get', 'post'])
def login():
    form1 = LoginForm()
    if form1.validate_on_submit():
        user = Students.query.filter_by(username=form1.name.data).first()
        if user is not None and user.verify_password(form1.password.data):
            login_user(user, form1.remember_me.data)
            flash(u'登录成功.')
            return redirect(url_for('main.welcomepage'))
    return render_template('user_login.html', Form=form1)


# 登录
@main.route('/login', methods=['get', 'post'])
def login():
    form1 = LoginForm()
    if form1.validate_on_submit():
        user = Students.query.filter_by(username=form1.name.data).first()
        if user is not None and user.verify_password(form1.password.data):
            login_user(user, form1.remember_me.data)
            flash(u'登录成功.')
            return redirect(url_for('main.welcomepage'))
        else:
            flash(u'用户名或密码有错误.')
    return render_template('user_login.html', Form=form1)


# 注册
@main.route('/reg', methods=['get', 'post'])
def reg():
    form = NameForm()
    if form.validate_on_submit():
        user = Students(username=form.name.data, password=form.password.data,
                    email=form.mail.data, nickname=form.nickname.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'confirm', user=user, token=token)
        flash(u'一封确认邮件已经发送到你的邮箱里.请登录后用当前浏览器打开邮件中的网站完成确认')
        return redirect(url_for('main.login'))
    return render_template('reg.html', Form=form)



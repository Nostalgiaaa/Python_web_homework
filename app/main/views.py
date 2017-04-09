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

# 主页面
@main.route('/', methods=['get'])
def welcomepage():
    return render_template('welcome.html')


# 登录
@main.route('/login', methods=['get', 'post'])
def login():
    form1 = LoginForm()
    if form1.validate_on_submit():
        user = Manager.query.filter_by(Id=form1.name.data).first()
        if user is not None: #and user.verify_password(form1.password.data):
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
        return redirect(url_for('main.login'))
    return render_template('reg.html', Form=form)


# 登出
@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.welcomepage'))









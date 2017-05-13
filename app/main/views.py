#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import main
from datetime import datetime
from flask import render_template, session, redirect, url_for, request, flash, current_app
from . import main
from .forms import *
from ..__init__ import db
from ..models import *
from flask_login import login_user
from flask_login import logout_user, login_required
from flask_login import current_user
import time


# 主页面
@main.route('/', methods=['get'])
def welcomepage():
    return render_template('welcome.html')


# 管理员界面
@login_required
@main.route('/manager', methods=['get', 'post'])
def manager_page():
    form_regstudent = RegStudent()  # 按班级添加的表单
    form_regstudent_one = RegStudent_one()  # 按个人添加的表单
    form_password = RegStudent_password()    # 重设学生密码
    form_regteacher = Regteacher()  # 添加老师的表单
    form_teacher_password = Regteacher_password()  # 重设教师密码
    # 同一个页面两个表单提交的时候，因为validate_on_submit只会判断是否post，从而提交第二个表单也会走第一个if代码块，所以首先判断
    # 两个表单的submit是否有值，参考https://zhuanlan.zhihu.com/p/23437362
    if form_regstudent.submit.data and form_regstudent.validate_on_submit():
        Id = form_regstudent.grade.data + form_regstudent.typenum.data + form_regstudent.classnum.data
        for every in xrange(1, int(form_regstudent.studentnum.data) + 1):
            if every < 10:
                studentid = Id + '0' + str(every)
            else:
                studentid = Id + str(every)
            user = Students(Id=studentid, password='lgd123456', email='None')
            db.session.add(user)
        db.session.commit()
        flash(u'班级添加成功.')
        return redirect(url_for('main.manager_page'))
    if form_regstudent_one.submit_one.data and form_regstudent_one.validate_on_submit():
        Id = form_regstudent.grade.data + form_regstudent.typenum.data + form_regstudent.classnum.data +form_regstudent.studentnum.data
        user = Students(Id=Id, password='lgd123456', email='None')
        db.session.add(user)
        db.session.commit()
        flash(u'单个学生添加成功.')
        return redirect(url_for('main.manager_page'))

    if form_password.submit_password.data and form_password.validate_on_submit():
        Id = form_regstudent.studentnum.data
        user = Students.query.filter_by(Id=Id).first()
        user.password = '123456789'
        db.session.commit()
        flash(u'重置密码成功.')
        return redirect(url_for('main.manager_page'))

    if form_regteacher.submit_teacher.data and form_regteacher.validate_on_submit():
        Id = form_regteacher.teachernum.data
        user = Teacher(Id=Id, password='teacher123456', email='None')
        db.session.add(user)
        db.session.commit()
        flash(u'添加教师成功.')
        return redirect(url_for('main.manager_page'))

    if form_teacher_password.submit_password_teacher.data and form_teacher_password.validate_on_submit():
        Id = form_teacher_password.teachernum_password.data
        user = Teacher.query.filter_by(Id=Id).first()
        user.password = 'teacher123456'
        db.session.commit()
        flash(u'重置密码成功.')
        return redirect(url_for('main.manager_page'))

    return render_template('manager_page.html')


# 学生界面
@login_required
@main.route('/student', methods=['get', 'post'])
def student_page():
    return render_template('student_page.html')


# 教师界面
@login_required
@main.route('/teacher_page', methods=['get', 'post'])
def teacher_page():
    form_addclass = AddClass()
    form_deleteclass = DeleteClass()
    form_changeclass = ChangeClass()
    if form_addclass.submit_addclass.data and form_addclass.validate_on_submit():
        name = form_addclass.class_name.data
        teacher_class = TeachClass(teacher_id=current_user.Id, class_name=name)
        db.session.add(teacher_class)
        db.session.commit()
        flash(u'添加课程信息成功.')
        return redirect(url_for('main.teacher_page'))
    if form_deleteclass.submit_deleteclass.data and form_deleteclass.validate_on_submit():
        name = form_deleteclass.class_name_delete.data
        delete_class = TeachClass.query.filter_by(class_name=name, teacher_id=current_user.Id).first()
        db.session.delete(delete_class)
        db.session.commit()
        flash(u'删除课程信息成功.')
        return redirect(url_for('main.teacher_page'))
    if form_changeclass.submit_changeclass.data and form_changeclass.validate_on_submit():
        name = form_changeclass.class_name_change.data
        after_name = form_changeclass.class_name_after_change.data
        print after_name
        change_class = TeachClass.query.filter_by(class_name=name, teacher_id=current_user.Id).first()
        change_class.class_name = after_name
        db.session.commit()
        flash(u'修改课程信息成功.')
        return redirect(url_for('main.teacher_page'))
    return render_template('teacher_page.html')


# 管理员管理学生界面
@login_required
@main.route('/student_work', methods=['get', 'post'])
def student_work():
    return render_template('student_work.html')


# 管理员管理学生界面
@login_required
@main.route('/manager_student', methods=['get', 'post'])
def manager_student():
    form_regstudent = RegStudent()
    form_regstudent_one = RegStudent_one()
    form_password = RegStudent_password()
    return render_template('manager_student.html', Form=form_regstudent, Form_student_one=form_regstudent_one, Form_password=form_password)


# 管理员管理教师界面
@login_required
@main.route('/manager_teacher', methods=['get', 'post'])
def manager_teacher():
    form_regteacher = Regteacher()
    form_teacher_password = Regteacher_password()
    return render_template('manager_teacher.html', Form_teacher=form_regteacher, Form_password_teacher=form_teacher_password)


# 教师界面
@login_required
@main.route('/teacher_class', methods=['get', 'post'])
def teacher_class():
    class_list = TeachClass.query.filter_by(teacher_id=current_user.Id)
    return_list = []
    for class_ in class_list:
        return_list.append(
            [class_.class_id, class_.class_name]
        )
    form_addclass = AddClass()
    form_deleteclass = DeleteClass()
    form_changeclass = ChangeClass()
    return render_template('teacher_class.html', return_list=return_list, Form_addclass=form_addclass,
                           Form_deleteclass=form_deleteclass, Form_changeclass=form_changeclass,
                           )


# 登录
@main.route('/login', methods=['get', 'post'])
def login():
    form1 = LoginForm()
    if form1.validate_on_submit() and form1.type.data == u'管理员':  # 管理员登录
        user = Manager.query.filter_by(Id=form1.name.data).first()
        if user is not None: #and user.verify_password(form1.password.data):
            login_user(user, form1.remember_me.data)
            flash(u'登录成功.')
            return redirect(url_for('main.manager_page'))
        else:
            flash(u'用户名或密码有错误.')
    if form1.validate_on_submit() and form1.type.data == u'学生':
        user = Students.query.filter_by(Id=form1.name.data).first()
        if user is not None and user.verify_password(form1.password.data):
            login_user(user, form1.remember_me.data)
            flash(u'登录成功.')
            return redirect(url_for('main.student_page'))
        else:
            flash(u'用户名或密码有错误.')
    if form1.validate_on_submit() and form1.type.data == u'教师':
        user = Teacher.query.filter_by(Id=form1.name.data).first()
        if user is not None and user.verify_password(form1.password.data):
            login_user(user, form1.remember_me.data)
            flash(u'登录成功.')
            return redirect(url_for('main.teacher_page'))
        else:
            flash(u'用户名或密码有错误.')
    return render_template('user_login.html', Form=form1)


# 登出
@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.welcomepage'))









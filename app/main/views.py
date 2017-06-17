#!/usr/bin/env python
# -*- coding: utf-8 -*-

from werkzeug.utils import secure_filename
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
from flask import send_from_directory
import os
basedir = os.path.abspath(os.path.dirname(__file__))


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
    handel_work = HandelWork()
    download_work = DownloadWork()
    if handel_work.submit_file.data and handel_work.validate_on_submit():
        file = handel_work.file.data
        fname = secure_filename(file.filename)
        ext = fname.rsplit('.', 1)[1]
        PATH = '/work'
        file_name = str(current_user.Id) + '_' + handel_work.homework_id.data + '.' + ext
        file_dir = basedir + PATH
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        flash(u'上传成功')
        add_work = HomeWorkStudent.query.filter_by(student_id=current_user.Id, homework_id=handel_work.homework_id.data).first()
        add_work.store_place = file_name
        db.session.commit()
        file.save(os.path.join(file_dir, file_name))
        return redirect(url_for('main.student_page'))
    if download_work.submit_file_download.data and download_work.validate_on_submit():
        file_dir = basedir + '/work'
        add_work = HomeWorkStudent.query.filter_by(student_id=current_user.Id,
                                                   homework_id=handel_work.homework_id.data).first()
        file_name = add_work.store_place
        return send_from_directory(file_dir, file_name, as_attachment=True)
    return render_template('student_page.html')


# 教师界面
@login_required
@main.route('/teacher_page', methods=['get', 'post'])
def teacher_page():
    form_addclass = AddClass()
    form_deleteclass = DeleteClass()
    form_changeclass = ChangeClass()
    form_addwork = AddWork()
    form_deletework = DeleteWork()
    form_change_work = ChangeWork()
    form_add_student_work = AddStudentWork()
    form_student_work_score = AddStudentWorkScore()
    form_download_work = DownloadWork()
    form_message = AddMsg()
    if form_message.submit_add_msg.data and form_message.validate_on_submit():
        sent_id = current_user.Id
        be_sent_id = form_message.be_sent_id.data
        msg = form_message.msg.data
        times = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        msg_ = Message(sent_msg=sent_id, be_sent_msg=be_sent_id, time=times, msg=msg)
        db.session.add(msg_)
        db.session.commit()
        flash(u'添加消息成功.')
        return redirect(url_for('main.teacher_page'))

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
    if form_addwork.submit_add_work.data and form_addwork.validate_on_submit():
        class_id = form_addwork.class_id.data
        work_name = form_addwork.work_name.data
        end_date = form_addwork.end_date.data
        add_work = HomeWork(class_id=class_id, homework_name=work_name, end_date=end_date, teacher_id=current_user.Id)
        db.session.add(add_work)
        db.session.commit()
        flash(u'增加作业成功.')
        return redirect(url_for('main.teacher_page'))
    if form_deletework.submit_delete_work.data and form_deletework.validate_on_submit():
        work_name = form_deletework.work_name_delete.data
        delete_work = HomeWork.query.filter_by(homework_id=work_name).first()
        db.session.delete(delete_work)
        db.session.commit()
        flash(u'删除作业成功.')
        return redirect(url_for('main.teacher_page'))

    if form_change_work.submit_change_work.data and form_change_work.validate_on_submit():
        id = form_change_work.work_id.data
        name_new = form_change_work.work_name_after_change.data
        end_date_new = form_change_work.end_date_after_change.data
        change_work = HomeWork.query.filter_by(homework_id=id).first()
        if name_new:
            change_work.homework_name = name_new
        if end_date_new:
            change_work.end_date = end_date_new
        db.session.commit()
        flash(u'修改作业信息成功.')
        return redirect(url_for('main.teacher_page'))
    if form_add_student_work.submit_add_student_work.data and form_add_student_work.validate_on_submit():
        student_id = form_add_student_work.student_id.data
        homework_id = form_add_student_work.homework_id.data
        add_work = HomeWorkStudent(student_id=student_id, homework_id=homework_id)
        db.session.add(add_work)
        db.session.commit()
        flash(u'分配作业成功.')
        return redirect(url_for('main.teacher_page'))
    if form_student_work_score.submit_add_student_work_score.data and form_student_work_score.validate_on_submit():
        student_id = form_student_work_score.student_id.data
        homework_id = form_student_work_score.homework_id.data
        score = form_student_work_score.score.data
        assign = form_student_work_score.assign.data
        add_score = HomeWorkStudent.query.filter_by(student_id=student_id, homework_id=homework_id).first()
        add_score.score = score
        add_score.comment = assign
        db.session.commit()
        flash(u'打分，评语成功.')
        return redirect(url_for('main.teacher_page'))
    if form_download_work.submit_file_download.data and form_download_work.validate_on_submit():
        file_dir = basedir + '/work'
        add_work = HomeWorkStudent.query.filter_by(student_id=form_download_work.student_id.data,
                                                   homework_id=form_download_work.homework_id.data).first()
        if not add_work:
            flash(u'未分配作业或填写有错.')
            return redirect(url_for('main.teacher_page'))
        file_name = add_work.store_place
        if not file_name:
            flash(u'该学生还未上交作业.')
            return redirect(url_for('main.teacher_page'))
        file_name = add_work.store_place
        return send_from_directory(file_dir, file_name, as_attachment=True)
    return render_template('teacher_page.html')


# 管理员管理学生界面
@login_required
@main.route('/student_work', methods=['get', 'post'])
def student_work():
    handel_work = HandelWork()
    download_work = DownloadWork()
    return render_template('student_work.html', Form_handel_work=handel_work, Form_download_work=download_work)


# 学生查看信息
@login_required
@main.route('/student_message', methods=['get', 'post'])
def student_message():
    message = Message.query.filter_by(be_sent_msg=current_user.Id)
    return_list = []
    for i in message:
        return_list.append(
            {
                'sent_msg': i.sent_msg,
                'time': i.time,
                'msg': i.msg
            }
        )
    return_list = return_list[::-1]
    return render_template('student_message.html', return_list=return_list)


# 学生查看评分界面
@login_required
@main.route('/student_score', methods=['get', 'post'])
def student_score():
    return_list = []
    student_id = current_user.Id
    class_list = HomeWorkStudent.query.filter_by(student_id=student_id)
    for i in class_list:
        homework_id = i.homework_id
        class_name = HomeWork.query.filter_by(homework_id=homework_id).first()
        class_name_ = class_name.homework_name
        end_data = class_name.end_date
        return_list.append(
            [i.score, i.comment, class_name_, end_data]
        )
    return render_template('student_score.html', return_list=return_list)

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


# 教师管理课程界面
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


# 教师管理作业界面
@login_required
@main.route('/teacher_work', methods=['get', 'post'])
def teacher_work():
    work_list = HomeWork.query.filter_by(teacher_id=current_user.Id)
    return_list = []
    form_addwork = AddWork()
    form_delete_work = DeleteWork()
    form_change_work = ChangeWork()
    form_add_student_work = AddStudentWork()
    for work_ in work_list:
        return_list.append(
            [work_.homework_id, work_.class_id, work_.homework_name, work_.end_date]
        )
    return render_template('teacher_work.html', return_list=return_list, Form_addwork=form_addwork,
                           Form_delete_work=form_delete_work, Form_change_work=form_change_work,
                           Form_add_student_work=form_add_student_work,
                           )


# 教师管理评分界面
@login_required
@main.route('/teacher_score', methods=['get', 'post'])
def teacher_score():
    form_student_work_score = AddStudentWorkScore()
    form_download_work = DownloadWork()
    return render_template('teacher_score.html', Form_student_work_score=form_student_work_score,
                           Form_download_work=form_download_work
                           )


# 教师发布信息界面
@login_required
@main.route('/teacher_message', methods=['get', 'post'])
def teacher_message():
    form_message = AddMsg()
    return render_template('teacher_message.html', Form_message=form_message)


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









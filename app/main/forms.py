#coding:utf-8
from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField
from wtforms.validators import Required, ValidationError, InputRequired, Email
from flask_wtf.file import FileField, FileRequired, FileAllowed
from ..models import *
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ..models import Students, Teacher

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

def teachernumcheck(form, field):
    if not Teacher.query.filter_by(Id=field.data).first():
        raise ValidationError(u'学号不存在')





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
    submit_password = SubmitField(u'确认修改个人')


class Regteacher(Form):
    teachernum = StringField(u'教师账号', validators=[InputRequired(), usercheck])
    submit_teacher = SubmitField(u'确认添加个人')


class Regteacher_password(Form):
    teachernum_password = StringField(u'教工号', validators=[InputRequired(), teachernumcheck])
    submit_password_teacher = SubmitField(u'确认修改密码')


class AddClass(Form):
    class_name = StringField(u'课程名', validators=[InputRequired()])
    submit_addclass = SubmitField(u'确认添加')


class DeleteClass(Form):
    class_name_delete = StringField(u'课程名', validators=[InputRequired()])
    submit_deleteclass = SubmitField(u'确认删除')


class ChangeClass(Form):
    class_name_change = StringField(u'原来课程名', validators=[InputRequired()])
    class_name_after_change = StringField(u'新课程名', validators=[InputRequired()])
    submit_changeclass = SubmitField(u'确认修改')


class AddWork(Form):
    work_name = StringField(u'作业名', validators=[InputRequired()])
    class_id = StringField(u'课程id', validators=[InputRequired()])
    end_date = StringField(u'截止日期', validators=[InputRequired()])
    submit_add_work = SubmitField(u'确认添加')


class DeleteWork(Form):
    work_name_delete = StringField(u'作业id', validators=[InputRequired()])
    submit_delete_work = SubmitField(u'确认删除')


class ChangeWork(Form):
    work_id = StringField(u'要修改的作业id', validators=[InputRequired()])
    work_name_after_change = StringField(u'新课程名，不填即为不修改', validators=[])
    end_date_after_change = StringField(u'新截止日期,不填即为不修改', validators=[])
    submit_change_work = SubmitField(u'确认修改')


class AddStudentWork(Form):
    student_id = StringField(u'学生id', validators=[InputRequired()])
    homework_id = StringField(u'作业id', validators=[InputRequired()])
    submit_add_student_work = SubmitField(u'确认添加')


class AddStudentWorkScore(Form):
    student_id = StringField(u'学生id', validators=[InputRequired()])
    homework_id = StringField(u'作业id', validators=[InputRequired()])
    score = StringField(u'分数', validators=[InputRequired()])
    assign = StringField(u'评语', validators=[InputRequired()])
    submit_add_student_work_score = SubmitField(u'确认添加')


class HandelWork(Form):
    homework_id = StringField(u'作业id', validators=[InputRequired()])
    file = FileField(u'上传文件', validators=[
        # FileAllowed(['txt', 'doc', 'image', 'excel'], u'只能上传文档！'),
        FileRequired(u'文件未选择！')
    ])
    submit_file = SubmitField(u'确认提交')


class DownloadWork(Form):
    student_id = StringField(u'学生id', validators=[InputRequired()])
    homework_id = StringField(u'作业id', validators=[InputRequired()])
    submit_file_download = SubmitField(u'下载作业')


class AddMsg(Form):
    be_sent_id = StringField(u'接受者id', validators=[InputRequired()])
    msg = StringField(u'评语', validators=[InputRequired()])
    submit_add_msg = SubmitField(u'确认添加')

# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp
from models.users import User
from models.roles import Role
from flask_pagedown.fields import PageDownField
from flask_ckeditor import CKEditorField


# 修改资料的form
class EditProfileForm(FlaskForm):
    name = StringField('Your name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


# 管理员使用的资料编辑表单
class EditProfileAdminForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 64), Regexp(
        '^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, numbers, dots or underscores')])
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        # 旧类无法使用新的super方法
        FlaskForm.__init__(self, *args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


# 博客填写表单，首页显示
class BlogForm(FlaskForm):
    body = PageDownField('Write your blog:', validators=[DataRequired()])
    submit = SubmitField('Submit')


# 评论填写表单
class CommentForm(FlaskForm):
    body = StringField('Write your comment:', validators=[DataRequired()])
    submit = SubmitField('Submit')

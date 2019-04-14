# -*- coding: utf-8 -*-
from config import db
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from models.roles import Role, Perm
from config import login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(64), unique=True)
    # 设置外键
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password = db.Column(db.String(64))
    confirmed = db.Column(db.Boolean, default=False)
    location = db.Column(db.Text())
    about_me = db.Column(db.Text())

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            # 将kangming的权限设置为管理员
            if self.username == 'kangming':
                self.role = Role.query.filter_by(name='Administrator').first()
            # 如果未指定role，则为默认权限，即User
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def generate_confirmation_token(self, expiration=300):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        data = s.loads(token.encode('utf-8'))
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        # 添加手动commit，是否有必要？
        db.session.commit()
        return True

    # 确认密码是否正确
    def verify_password(self, password):
        if self.password == password:
            return True
        else:
            return False

    # 检查是否有指定权限
    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    # 检查是否有管理员权限
    def is_administrator(self):
        return self.can(Perm.A)


class AnonymousUser(AnonymousUserMixin):
    @staticmethod
    def can(perm):
        return False

    @staticmethod
    def is_administrator():
        return False


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

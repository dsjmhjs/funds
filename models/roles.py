# -*- coding: utf-8 -*-
from config import db


# 权限常量，对应用户权限位置上的标志位，故均为2的n次方
# Permission
class Perm:
    # FOLLOW：关注
    F = 1
    # COMMENT：评论
    C = 2
    # WRITE：写文章
    W = 4
    # MODERATE：管理评论
    M = 8
    # ADMIN：管理员
    A = 16

    def __init__(self):
        pass


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        # 若插入角色时不设置权限，默认为0
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Perm.F, Perm.C, Perm.W],
            'Moderator': [Perm.F, Perm.C, Perm.W, Perm.M],
            'Administrator': [Perm.F, Perm.C, Perm.W, Perm.M, Perm.A],
        }
        default_role = 'User'
        # 遍历三个角色
        for r in roles:
            # 获取数据库角色表中某一个角色
            role = Role.query.filter_by(name=r).first()
            # 若无该角色
            if role is None:
                # 构建角色对象
                role = Role(name=r)
            # 先重置角色权限
            role.reset_permissions()
            # 遍历每个角色对应的几项权限，依次添加
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name

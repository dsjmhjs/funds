# -*- coding: utf-8 -*-

from config import db
from models.users import User
from models.roles import Role
from faker import Faker
from sqlalchemy.exc import IntegrityError
# 上下文
from start import create_app


def mydb_init():
    db.create_all()


def mydb_set_users():
    users = User.query.all()
    roles = Role.query.all()
    for user in users:
        db.session.delete(user)
    for role in roles:
        db.session.delete(role)
    Role.insert_roles()

    # make_users()

    km = User(username='kangming', password='123456', email='451221245@qq.com')
    km.confirmed = True
    km.location = 'Beijing'
    km.about_me = 'The longest day has an end.'
    db.session.add(km)

    db.session.commit()


def make_users(count=5):
    fake = Faker()
    i = 1
    while i < count:
        user = User(username='user' + str(i),
                    email=fake.email(),
                    password='password',
                    confirmed=True,
                    location=fake.city(),
                    about_me=fake.text())
        db.session.add(user)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()


if __name__ == '__main__':
    with create_app('default').app_context():
        mydb_init()

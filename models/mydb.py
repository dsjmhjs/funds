# -*- coding: utf-8 -*-

from config import db
from models.users import User
from models.roles import Role
from models.funds import Fund
from faker import Faker
from sqlalchemy.exc import IntegrityError
# wind
from WindPy import *
from datetime import datetime


def mydb_init():
    db.drop_all()
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


def mydb_set_funds():
    # 删除旧数据
    funds = Fund.query.all()
    for fund in funds:
        db.session.delete(fund)
    today = datetime.now().strftime("%Y-%m-%d")
    w.start()
    # 获取全部基金
    # [[wind_code]]
    funds_data = w.wset("sectorconstituent",
                        "date=" + today + ";sectorid=a201010700000000;field=wind_code").Data
    funds_code = funds_data[0]
    length = len(funds_code)
    # 获取基金详情
    # [[sec_name,fund_type,fund_investtype,fund_trackindexcode,fund_fundscale,fund_mgrcomp,fund_fundmanager],[]...]
    funds_detail = []
    for i in range(0, length):
        fund_detail = w.wss(funds_code[i],
                             "sec_name,fund_type,fund_investtype,fund_trackindexcode,fund_fundscale,fund_mgrcomp,fund_fundmanager").Data
        funds_detail.append([
            funds_code[i],
            fund_detail[0][0],
            fund_detail[1][0],
            fund_detail[2][0],
            fund_detail[3][0],
            fund_detail[4][0],
            fund_detail[5][0],
            fund_detail[6][0]]
        )
        if i < length - 1:
            print 'The next is ' + funds_code[i + 1]
    w.stop()
    # 写入新数据
    # for i in range(0, length):
    #     fund = Fund(
    #         date=today,
    #         wind_code=funds_codes[i],
    #         sec_name=funds_detail[0][i],
    #         fund_type=funds_detail[1][i],
    #         fund_investtype=funds_detail[2][i],
    #         fund_trackindexcode=funds_detail[3][i],
    #         fund_fundscale=funds_detail[4][i],
    #         fund_mgrcomp=funds_detail[5][i],
    #         fund_fundmanager=funds_detail[6][i]
    #     )
    #     db.session.add(fund)
    # db.session.commit()

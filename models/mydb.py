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
from threading import Lock
import threadpool

count = 0
lock = Lock()


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
    for f in funds:
        db.session.delete(f)
    db.session.commit()
    today = datetime.now().strftime("%Y-%m-%d")
    w.start()
    # 获取全部基金
    # [[wind_code]]
    funds_data = w.wset("sectorconstituent",
                        "date=" + today + ";sectorid=a201010700000000;field=wind_code").Data
    # 基金列表
    funds_code = funds_data[0]
    # 拼接成的以,分隔的字符串，每100个一组
    funds_str = []
    p = 0
    while p < len(funds_code):
        funds_str_part = ''
        for i in range(100):
            if p >= len(funds_code):
                break
            funds_str_part += (funds_code[p] + ',')
            p += 1
        funds_str_part = funds_str_part[:-1]
        funds_str.append(funds_str_part)

    # 获取基金详情
    # [[today...],[wind_code...],[sec_name...]...]
    funds_detail = [[], [], [], [], [], [], []]
    for fs in funds_str:
        funds_detail_part = w.wss(fs,
                                  "sec_name,fund_type,fund_investtype,fund_trackindexcode,fund_fundscale,fund_mgrcomp,fund_fundmanager").Data
        for i in range(7):
            funds_detail[i] = funds_detail[i] + funds_detail_part[i]

    # def get_detail(fund_code):
    #     fund_detail = w.wss(fund_code,
    #                         "sec_name,fund_type,fund_investtype,fund_trackindexcode,fund_fundscale,fund_mgrcomp,fund_fundmanager").Data
    #     funds_detail.append([
    #         today,
    #         fund_code,
    #         fund_detail[0][0],
    #         fund_detail[1][0],
    #         fund_detail[2][0],
    #         fund_detail[3][0],
    #         fund_detail[4][0],
    #         fund_detail[5][0],
    #         fund_detail[6][0]
    #     ])

    # 利用线程池获取基金详情，加快获取速度
    # pool = threadpool.ThreadPool(5)
    # requests = threadpool.makeRequests(get_detail, funds_code)
    # [pool.putRequest(req) for req in requests]
    # pool.wait()

    w.stop()
    # 写入新数据
    for i in range(0, len(funds_code)):
        fund = Fund(
            date=today,
            wind_code=funds_code[i],
            sec_name=funds_detail[0][i],
            fund_type=funds_detail[1][i],
            fund_investtype=funds_detail[2][i],
            fund_trackindexcode=funds_detail[3][i],
            fund_fundscale=funds_detail[4][i],
            fund_mgrcomp=funds_detail[5][i],
            fund_fundmanager=funds_detail[6][i]
        )
        db.session.add(fund)
    db.session.commit()

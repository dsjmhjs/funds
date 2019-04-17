# -*- coding: utf-8 -*-

from config import db
from models.users import User
from models.roles import Role
from models.funds import Fund, TrackIndex
from faker import Faker
from sqlalchemy.exc import IntegrityError
# wind
from WindPy import *
from datetime import datetime
# 上下文
from start import create_app


# from threading import Lock
# import threadpool


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
    # 因基金数量较多，windpy接口参数不支持过长字符串，故分割为长度为100的子串
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
    count = 0
    for fs in funds_str:
        print count
        count += 100
        funds_detail_part = w.wss(fs,
                                  "sec_name,fund_firstinvesttype,fund_investtype,fund_trackindexcode,fund_fundscale,fund_mgrcomp,fund_fundmanager").Data
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
            fund_firstinvesttype=funds_detail[1][i],
            fund_investtype=funds_detail[2][i],
            fund_trackindexcode=funds_detail[3][i],
            fund_fundscale=funds_detail[4][i],
            fund_mgrcomp=funds_detail[5][i],
            fund_fundmanager=funds_detail[6][i]
        )
        db.session.add(fund)
    db.session.commit()


def mydb_set_trackindexes():
    # 删除旧数据
    trackindexes = TrackIndex.query.all()
    for ti in trackindexes:
        db.session.delete(ti)
    db.session.commit()
    # 从funds表中获取跟踪指数信息
    funds = Fund.query.filter(Fund.fund_trackindexcode != None).all()
    fund_trackindexcodes = set()
    for f in funds:
        fund_trackindexcodes.add(f.fund_trackindexcode)
    fund_trackindexcodes = list(fund_trackindexcodes)
    # 获取每一只跟踪指数的历史数据
    today = datetime.now().strftime("%Y-%m-%d")
    # w.wsd("H30165.CSI", "pe_ttm", "2019-03-17", "2019-04-15", "")
    w.start()
    count = 0
    for fti in fund_trackindexcodes:
        print count, fti
        count += 1
        detail = w.wsd(fti, "sec_name,pe_ttm,pb_lf", "2000-01-01", today, "")
        times = detail.Times
        data = detail.Data
        for i in range(0, len(times)):
            trackindex = TrackIndex(
                date=times[i],
                wind_code=fti,
                sec_name=data[0][i],
                pe_ttm=data[1][i],
                pb_lf=data[2][i]
            )
            db.session.add(trackindex)
    db.session.commit()
    w.stop()


if __name__ == '__main__':
    with create_app('default').app_context():
        mydb_set_trackindexes()

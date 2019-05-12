# -*- coding: utf-8 -*-

from config import db
from models.funds import Fund
# wind
from WindPy import *
from datetime import datetime
# 上下文
from start import create_app

today = datetime.now().strftime("%Y-%m-%d")


def mydb_set_funds():
    # 删除旧数据
    funds = Fund.query.all()
    for f in funds:
        db.session.delete(f)
    db.session.commit()
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
        funds_detail_part = w.wss(
            fs,
            "sec_name,fund_firstinvesttype,fund_investtype,fund_trackindexcode,fund_fundscale,fund_mgrcomp,fund_fundmanager"
        ).Data
        for i in range(7):
            funds_detail[i] = funds_detail[i] + funds_detail_part[i]
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
            fund_fundscale=none2zero(funds_detail[4][i]),
            fund_mgrcomp=funds_detail[5][i],
            fund_fundmanager=funds_detail[6][i]
        )
        db.session.add(fund)
    db.session.commit()


def none2zero(x):
    if x is None:
        return 0
    else:
        return x


if __name__ == '__main__':
    with create_app('default').app_context():
        mydb_set_funds()

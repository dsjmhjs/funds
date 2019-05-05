# -*- coding: utf-8 -*-

from config import db
from models.funds import Fund, TrackIndex, ShowIndex
# wind
from WindPy import *
from datetime import datetime
# 上下文
from start import create_app

today = datetime.now().strftime("%Y-%m-%d")


# 从wind获取跟踪指数历史数据，为防止因条数太多而受限，以周频率提取
def mydb_set_trackindexes():
    # 删除旧数据
    # trackindexes = TrackIndex.query.all()
    # for ti in trackindexes:
    #     db.session.delete(ti)
    # db.session.commit()
    # 从funds表中获取跟踪指数信息
    funds_filters = {
        Fund.fund_investtype == u'被动指数型基金',
        Fund.fund_trackindexcode != ''
    }
    columns = Fund.fund_trackindexcode
    entities = Fund.query.filter(*funds_filters).with_entities(columns).group_by(columns).all()
    fund_trackindexcodes = set()
    for entity in entities:
        fund_trackindexcodes.add(entity.fund_trackindexcode)
    fund_trackindexcodes = list(fund_trackindexcodes)
    w.start()
    # 获取每一只跟踪指数的发布日期
    # launchdate_dict = {}
    # for fti in fund_trackindexcodes:
    #     launchdate = w.wsd(fti, "launchdate", "2019-01-01", today, "Period=Y").Data[0][0]
    #     if launchdate != None:
    #         launchdate = launchdate.strftime("%Y-%m-%d")
    #     else:
    #         launchdate = "2010-01-01"
    #     if int(launchdate.split('-')[0]) < 2000:
    #         launchdate = "2000-01-01"
    #     print launchdate
    #     launchdate_dict.setdefault(fti, launchdate)
    # 获取每一只跟踪指数的历史数据
    count = 0
    for fti in fund_trackindexcodes:
        print count, fti
        count += 1
        # detail = w.wsd(fti, "sec_name,close,pe_ttm,pb_lf,ps_ttm", launchdate_dict[fti], today, "Period=W")
        # detail = w.wsd(fti, "sec_name,close,pe_ttm,pb_lf,ps_ttm", launchdate_dict[fti], "2018-12-31", "Period=W")
        # detail = w.wsd(fti, "sec_name,close,pe_ttm,pb_lf,ps_ttm", "2019-01-01", today, "")
        detail = w.wsd(fti, "sec_name,close,pe_ttm,pb_lf,ps_ttm", today, today, "")
        times = detail.Times
        data = detail.Data
        for i in range(0, len(times)):
            trackindex = TrackIndex(
                date=times[i],
                fund_trackindexcode=fti,
                sec_name=data[0][i],
                close=data[1][i],
                pe_ttm=data[2][i],
                pb_lf=data[3][i],
                ps_ttm=data[4][i]
            )
            db.session.add(trackindex)
    db.session.commit()
    w.stop()


def mydb_set_showindexes():
    showindexes = ShowIndex.query.all()
    for si in showindexes:
        db.session.delete(si)
    db.session.commit()
    funds_filters = {
        Fund.fund_investtype == u'被动指数型基金',
        Fund.fund_trackindexcode != ''
    }
    columns = Fund.fund_trackindexcode
    entities = Fund.query.filter(*funds_filters).with_entities(columns).group_by(columns).all()
    fund_trackindexcodes = set()
    for entity in entities:
        fund_trackindexcodes.add(entity.fund_trackindexcode)
    fund_trackindexcodes = list(fund_trackindexcodes)
    for fti in fund_trackindexcodes:
        fti_filters = {TrackIndex.fund_trackindexcode == fti}
        entities = TrackIndex.query.filter(*fti_filters).order_by(TrackIndex.date.desc()).first()
        showindex = ShowIndex(
            fund_trackindexcode=entities.fund_trackindexcode,
            sec_name=entities.sec_name,
            close=entities.close,
            pe_ttm=entities.pe_ttm,
            quantile='75%',
            pb_lf=entities.pb_lf,
            ps_ttm=entities.ps_ttm,
            date=entities.date
        )
        db.session.add(showindex)
    db.session.commit()


if __name__ == '__main__':
    with create_app('default').app_context():
        mydb_set_showindexes()

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
    trackindexes = TrackIndex.query.all()
    for ti in trackindexes:
        db.session.delete(ti)
    db.session.commit()
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
    launchdate_dict = {}
    for fti in fund_trackindexcodes:
        launchdate = w.wsd(fti, "launchdate", "2019-01-01", today, "Period=Y").Data[0][0]
        if launchdate != None:
            launchdate = launchdate.strftime("%Y-%m-%d")
        else:
            launchdate = "2010-01-01"
        if int(launchdate.split('-')[0]) < 2000:
            launchdate = "2000-01-01"
        print launchdate
        launchdate_dict.setdefault(fti, launchdate)
    # 获取每一只跟踪指数的历史数据
    count = 0
    for fti in fund_trackindexcodes:
        print count, fti
        count += 1
        detail = w.wsd(fti, "sec_name,close,pe_ttm,pb_lf,ps_ttm", launchdate_dict[fti], today, "Period=W")
        # detail = w.wsd(fti, "sec_name,close,pe_ttm,pb_lf,ps_ttm", today, today, "")
        times = detail.Times
        data = detail.Data
        for i in range(0, len(times)):
            trackindex = TrackIndex(
                date=times[i],
                fund_trackindexcode=fti,
                sec_name=data[0][i],
                close=none2zero(data[1][i]),
                pe_ttm=none2zero(data[2][i]),
                pb_lf=none2zero(data[3][i]),
                ps_ttm=none2zero(data[4][i])
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
        print fti
        fti_filters = {TrackIndex.fund_trackindexcode == fti}
        entities = TrackIndex.query.filter(*fti_filters).order_by(TrackIndex.date.desc()).first()
        start_dates = TrackIndex.query.filter(*fti_filters).order_by(TrackIndex.date).first()
        # 如果指数起始日晚于输入的起始时间，则略过该指数
        # if start_dates.date > start_time:
        #     continue
        count_filters = {
            Fund.fund_investtype == u'被动指数型基金',
            Fund.fund_trackindexcode == fti
        }
        count = Fund.query.filter(*count_filters).count()
        # 计算分位点
        pes = []
        fti_start_time_filters = {TrackIndex.fund_trackindexcode == fti}
        query_pes = TrackIndex.query.filter(*fti_start_time_filters).order_by(TrackIndex.pe_ttm).all()
        for query_pe in query_pes:
            if none2zero(query_pe.pe_ttm) != 0:
                pes.append(none2zero(query_pe.pe_ttm))
        length = len(pes)
        if length > 0:
            quantile = get_quantile(none2zero(entities.pe_ttm), pes)
            danger = pes[int(length * 0.75 - 1)]
            chance = pes[int(length * 0.25 - 1)]
        else:
            quantile = 1.0
            danger = 0.0
            chance = 0.0
        # 标记周期
        if start_dates.date <= '2006-07-01':
            cycle = 2006
        elif '2006-07-01' <= start_dates.date <= '2014-12-01':
            cycle = 2014
        else:
            cycle = 2025
        # 计算分周期分位点
        # 2006
        if cycle == 2006:
            fti_start_time_filters_2006 = {
                TrackIndex.fund_trackindexcode == fti,
                TrackIndex.date >= '2006-07-01'
            }
            query_pes_2006 = TrackIndex.query.filter(*fti_start_time_filters_2006).order_by(TrackIndex.pe_ttm).all()
            quantile_2006 = cal_quantile(query_pes_2006, entities.pe_ttm)
            quantile_2014 = 1.0
        # 2014
        elif cycle == 2014:
            fti_start_time_filters_2014 = {
                TrackIndex.fund_trackindexcode == fti,
                TrackIndex.date >= '2014-12-01'
            }
            query_pes_2014 = TrackIndex.query.filter(*fti_start_time_filters_2014).order_by(TrackIndex.pe_ttm).all()
            quantile_2014 = cal_quantile(query_pes_2014, entities.pe_ttm)
            quantile_2006 = 1.0
        else:
            quantile_2006 = 1.0
            quantile_2014 = 1.0
        showindex = ShowIndex(
            fund_trackindexcode=entities.fund_trackindexcode,
            sec_name=entities.sec_name,
            close=none2zero(entities.close),
            pe_ttm=none2zero(entities.pe_ttm),
            quantile=quantile,
            danger=danger,
            chance=chance,
            pb_lf=none2zero(entities.pb_lf),
            ps_ttm=none2zero(entities.ps_ttm),
            start_date=start_dates.date,
            date=entities.date,
            count=count,
            cycle=cycle,
            quantile_2006=quantile_2006,
            quantile_2014=quantile_2014
        )
        db.session.add(showindex)
    db.session.commit()


def cal_quantile(qpes, pt):
    pes = []
    for qpe in qpes:
        if none2zero(qpe.pe_ttm) != 0:
            pes.append(none2zero(qpe.pe_ttm))
    length = len(pes)
    if length > 0:
        quantile = get_quantile(none2zero(pt), pes)
    else:
        quantile = 1.0
    return quantile


def get_quantile(pe, pes):
    length = len(pes)
    for i in range(length):
        if pe < pes[i]:
            return float(i - 1) / float(length)
    return float(1)


def none2zero(x):
    if x is None:
        return 0
    else:
        return x


if __name__ == '__main__':
    with create_app('default').app_context():
        # mydb_set_trackindexes()
        mydb_set_showindexes()

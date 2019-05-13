# -*- coding: utf-8 -*-

from config import db


class Fund(db.Model):
    __tablename__ = 'funds'
    id = db.Column(db.Integer, primary_key=True)
    # 获取日期
    date = db.Column(db.String(64))
    # wind代码
    wind_code = db.Column(db.String(64), unique=True)
    # 基金简称
    sec_name = db.Column(db.String(64))
    # 投资类型（一级分类）
    fund_firstinvesttype = db.Column(db.String(64))
    # 投资类型（二级分类）
    fund_investtype = db.Column(db.String(64))
    # 跟踪指数代码
    fund_trackindexcode = db.Column(db.String(64))
    # 基金规模
    fund_fundscale = db.Column(db.Float)
    # 基金管理人
    fund_mgrcomp = db.Column(db.String(64))
    # 基金经理
    fund_fundmanager = db.Column(db.String(64))


class TrackIndex(db.Model):
    __tablename__ = 'trackindexes'
    id = db.Column(db.Integer, primary_key=True)
    # 日期
    date = db.Column(db.String(64))
    # 指数代码
    fund_trackindexcode = db.Column(db.String(64))
    # 指数简称
    sec_name = db.Column(db.String(64))
    # 收盘价
    close = db.Column(db.Float)
    # 市盈率
    pe_ttm = db.Column(db.Float)
    # 市净率
    pb_lf = db.Column(db.Float)
    # 市销率
    ps_ttm = db.Column(db.Float)


class ShowIndex(db.Model):
    __tablename__ = 'showindexes'
    id = db.Column(db.Integer, primary_key=True)
    # 指数代码
    fund_trackindexcode = db.Column(db.String(64))
    # 指数简称
    sec_name = db.Column(db.String(64))
    # 收盘价
    close = db.Column(db.Float)
    # 市盈率
    pe_ttm = db.Column(db.Float)
    # 分位点
    quantile = db.Column(db.Float)
    # 危险值
    danger = db.Column(db.Float)
    # 机会值
    chance = db.Column(db.Float)
    # 市净率
    pb_lf = db.Column(db.Float)
    # 市销率
    ps_ttm = db.Column(db.Float)
    # 更新日期
    date = db.Column(db.String(64))
    # 基金数
    count = db.Column(db.Integer)

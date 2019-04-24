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
    fund_fundscale = db.Column(db.String(64))
    # 基金管理人
    fund_mgrcomp = db.Column(db.String(64))
    # 基金经理
    fund_fundmanager = db.Column(db.String(64))


class LXRIndice(db.Model):
    __tablename__ = 'lxrindices'
    id = db.Column(db.Integer, primary_key=True)
    # 日期
    date = db.Column(db.String(64))
    # 指数代码
    stock_code = db.Column(db.String(64))
    # 指数简称
    cn_name = db.Column(db.String(64))
    # 市盈率
    pe_ttm = db.Column(db.String(64))
    # 市净率
    pb = db.Column(db.String(64))
    # 市销率
    ps_ttm = db.Column(db.String(64))
    # 收盘点位
    cp = db.Column(db.String(64))
    # 市值
    mc = db.Column(db.String(64))


# track_code和indice_code的映射表
class TC2IC(db.Model):
    __tablename__ = 'tc2ics'
    id = db.Column(db.Integer, primary_key=True)
    # wind_code
    track_code = db.Column(db.String(64))
    # lxr_code
    indice_code = db.Column(db.String(64))
    cn_name = db.Column(db.String(64))

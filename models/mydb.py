# # -*- coding: utf-8 -*-
#
# from config import db
# from models.users import User
# from models.roles import Role
# from models.funds import Fund, LXRIndice, TC2IC
# from faker import Faker
# from sqlalchemy.exc import IntegrityError
# # wind
# from WindPy import *
# from datetime import datetime
# # 上下文
# from start import create_app
# # 请求处理
# import requests
# import json
# import time
#
# # from threading import Lock
# # import threadpool
#
#
# today = datetime.now().strftime("%Y-%m-%d")
#
#
# def mydb_init():
#     db.create_all()
#
#
# def mydb_set_users():
#     users = User.query.all()
#     roles = Role.query.all()
#     for user in users:
#         db.session.delete(user)
#     for role in roles:
#         db.session.delete(role)
#     Role.insert_roles()
#
#     # make_users()
#
#     km = User(username='kangming', password='123456', email='451221245@qq.com')
#     km.confirmed = True
#     km.location = 'Beijing'
#     km.about_me = 'The longest day has an end.'
#     db.session.add(km)
#
#     db.session.commit()
#
#
# def make_users(count=5):
#     fake = Faker()
#     i = 1
#     while i < count:
#         user = User(username='user' + str(i),
#                     email=fake.email(),
#                     password='password',
#                     confirmed=True,
#                     location=fake.city(),
#                     about_me=fake.text())
#         db.session.add(user)
#         try:
#             db.session.commit()
#             i += 1
#         except IntegrityError:
#             db.session.rollback()
#
#
# def mydb_set_funds():
#     # 删除旧数据
#     funds = Fund.query.all()
#     for f in funds:
#         db.session.delete(f)
#     db.session.commit()
#     w.start()
#     # 获取全部基金
#     # [[wind_code]]
#     funds_data = w.wset("sectorconstituent",
#                         "date=" + today + ";sectorid=a201010700000000;field=wind_code").Data
#     # 基金列表
#     funds_code = funds_data[0]
#     # 因基金数量较多，windpy接口参数不支持过长字符串，故分割为长度为100的子串
#     # 拼接成的以,分隔的字符串，每100个一组
#     funds_str = []
#     p = 0
#     while p < len(funds_code):
#         funds_str_part = ''
#         for i in range(100):
#             if p >= len(funds_code):
#                 break
#             funds_str_part += (funds_code[p] + ',')
#             p += 1
#         funds_str_part = funds_str_part[:-1]
#         funds_str.append(funds_str_part)
#
#     # 获取基金详情
#     # [[today...],[wind_code...],[sec_name...]...]
#     funds_detail = [[], [], [], [], [], [], []]
#     count = 0
#     for fs in funds_str:
#         print count
#         count += 100
#         funds_detail_part = w.wss(fs,
#                                   "sec_name,fund_firstinvesttype,fund_investtype,fund_trackindexcode,fund_fundscale,fund_mgrcomp,fund_fundmanager").Data
#         for i in range(7):
#             funds_detail[i] = funds_detail[i] + funds_detail_part[i]
#
#     # def get_detail(fund_code):
#     #     fund_detail = w.wss(fund_code,
#     #                         "sec_name,fund_type,fund_investtype,fund_trackindexcode,fund_fundscale,fund_mgrcomp,fund_fundmanager").Data
#     #     funds_detail.append([
#     #         today,
#     #         fund_code,
#     #         fund_detail[0][0],
#     #         fund_detail[1][0],
#     #         fund_detail[2][0],
#     #         fund_detail[3][0],
#     #         fund_detail[4][0],
#     #         fund_detail[5][0],
#     #         fund_detail[6][0]
#     #     ])
#
#     # 利用线程池获取基金详情，加快获取速度
#     # pool = threadpool.ThreadPool(5)
#     # requests = threadpool.makeRequests(get_detail, funds_code)
#     # [pool.putRequest(req) for req in requests]
#     # pool.wait()
#
#     w.stop()
#     # 写入新数据
#     for i in range(0, len(funds_code)):
#         fund = Fund(
#             date=today,
#             wind_code=funds_code[i],
#             sec_name=funds_detail[0][i],
#             fund_firstinvesttype=funds_detail[1][i],
#             fund_investtype=funds_detail[2][i],
#             fund_trackindexcode=funds_detail[3][i],
#             fund_fundscale=funds_detail[4][i],
#             fund_mgrcomp=funds_detail[5][i],
#             fund_fundmanager=funds_detail[6][i]
#         )
#         db.session.add(fund)
#     db.session.commit()
#
#
# # # 从wind获取跟踪指数历史数据，但因条数太多而受限
# # def mydb_set_trackindexes():
# #     # 删除旧数据
# #     trackindexes = TrackIndex.query.all()
# #     for ti in trackindexes:
# #         db.session.delete(ti)
# #     db.session.commit()
# #     # 从funds表中获取跟踪指数信息
# #     funds = Fund.query.filter(Fund.fund_trackindexcode != None).all()
# #     fund_trackindexcodes = set()
# #     for f in funds:
# #         fund_trackindexcodes.add(f.fund_trackindexcode)
# #     fund_trackindexcodes = list(fund_trackindexcodes)
# #     # 获取每一只跟踪指数的历史数据
# #     today = datetime.now().strftime("%Y-%m-%d")
# #     w.start()
# #     count = 0
# #     for fti in fund_trackindexcodes:
# #         print count, fti
# #         count += 1
# #         detail = w.wsd(fti, "sec_name,pe_ttm,pb_lf", "2000-01-01", today, "")
# #         times = detail.Times
# #         data = detail.Data
# #         for i in range(0, len(times)):
# #             trackindex = TrackIndex(
# #                 date=times[i],
# #                 wind_code=fti,
# #                 sec_name=data[0][i],
# #                 pe_ttm=data[1][i],
# #                 pb_lf=data[2][i]
# #             )
# #             db.session.add(trackindex)
# #     db.session.commit()
# #     w.stop()
#
#
# # 通过lxr数据接口导出
# def mydb_set_lxrindices():
#     # token
#     token = "d60faad6-7d91-4d02-a589-22d0cc937261"
#     # 删除旧数据
#     lxrindices = LXRIndice.query.all()
#     for lxrindice in lxrindices:
#         db.session.delete(lxrindice)
#     db.session.commit()
#     # 得到全部指数代码及成立时间
#     indices = get_indice_publishdate(token)
#     print '共', len(indices), '个指数'
#     # 根据indices获取每个指数的历史数据
#     count = 0
#     for indice in indices:
#         count += 1
#         print '第', count, '个'
#         if count % 50 == 0:
#             time.sleep(5)
#         stock_code = indice[0]
#         cn_name = indice[1]
#         publish_date = indice[2]
#         data_list = get_indice_fundamental(token, stock_code, publish_date, today)
#         for data in data_list:
#             lxrindice = LXRIndice(
#                 date=data[0],
#                 stock_code=stock_code,
#                 cn_name=cn_name,
#                 pe_ttm=data[1],
#                 pb=data[2],
#                 ps_ttm=data[3],
#                 cp=data[4],
#                 mc=data[5]
#             )
#             db.session.add(lxrindice)
#         db.session.commit()
#     print 'finished.'
#
#
# # 获取特定指数基本面信息
# def get_indice_fundamental(token, stock_code, start_date, end_date):
#     url = "https://open.lixinger.com/api/a/indice/fundamental"
#     headers = {"Content-Type": "application/json"}
#     param = {
#         "token": token,
#         "startDate": start_date,
#         "endDate": end_date,
#         "stockCodes": [
#             stock_code
#         ],
#         "metrics": [
#             # 加权平均滚动市盈率
#             "pe_ttm.weightedAvg",
#             # 加权平均市净率
#             "pb.weightedAvg",
#             # 加权平均滚动市销率
#             "ps_ttm.weightedAvg",
#             # 收盘点位
#             "cp",
#             # 市值
#             "mc"
#         ]
#     }
#     requests.DEFAULT_RETRIES = 5
#     s = requests.session()
#     s.keep_alive = False
#     r = s.post(url, headers=headers, json=param)
#     r_dict = json.loads(r.text)
#     data_dict_list = r_dict['data']
#     data_list = []
#     for data_dict in data_dict_list:
#         if 'date' in data_dict:
#             dt = data_dict['date'][:10]
#         else:
#             dt = '0000-00-00'
#         if 'pe_ttm' in data_dict and 'weightedAvg' in data_dict['pe_ttm']:
#             pe_ttm = data_dict['pe_ttm']['weightedAvg']
#         else:
#             pe_ttm = -1
#         if 'pb' in data_dict and 'weightedAvg' in data_dict['pb']:
#             pb = data_dict['pb']['weightedAvg']
#         else:
#             pb = -1
#         if 'ps_ttm' in data_dict and 'weightedAvg' in data_dict['ps_ttm']:
#             ps_ttm = data_dict['ps_ttm']['weightedAvg']
#         else:
#             ps_ttm = -1
#         if 'cp' in data_dict:
#             cp = data_dict['cp']
#         else:
#             cp = -1
#         if 'mc' in data_dict:
#             mc = data_dict['mc']
#         else:
#             mc = -1
#         data_list.append([dt, pe_ttm, pb, ps_ttm, cp, mc])
#     return data_list
#
#
# # 结构如下
# # {
# #   "code": 0,
# #   "msg": "success",
# #   "data": [
# #     {
# #       "date": "2019-04-04T00:00:00+08:00",
# #       "mc": 21014173498077.305,
# #       "pe_ttm": {
# #         "weightedAvg": 10.458130462139
# #       },
# #       "pb": {
# #         "weightedAvg": 1.2796918003351128
# #       },
# #       "ps_ttm": {
# #         "weightedAvg": 1.1587629027286634
# #       },
# #       "cp": 2951.98,
# #       "stockCode": "000016"
# #     },
# #     {
# #       "date": "2019-04-03T00:00:00+08:00",
# #       "mc": 20740096666326.105,
# #       "pe_ttm": {
# #         "weightedAvg": 10.32173055740965
# #       },
# #       "pb": {
# #         "weightedAvg": 1.2630014520667916
# #       },
# #       "ps_ttm": {
# #         "weightedAvg": 1.1436497665798755
# #       },
# #       "cp": 2920,
# #       "stockCode": "000016"
# #     }
# #   ]
# # }
#
#
# # 获取lxr全部指数代码及成立日期
# def get_indice_publishdate(token):
#     url = "https://open.lixinger.com/api/a/indice"
#     headers = {"Content-Type": "application/json"}
#     param = {
#         "token": token
#     }
#     requests.DEFAULT_RETRIES = 5
#     s = requests.session()
#     s.keep_alive = False
#     r = s.post(url, headers=headers, json=param)
#     r_dict = json.loads(r.text)
#     data_dict_list = r_dict['data']
#     data_list = []
#     for data_dict in data_dict_list:
#         stock_code = data_dict['stockCode']
#         cn_name = data_dict['cnName']
#         publish_date = data_dict['publishDate'][:10]
#         data_list.append([stock_code, cn_name, publish_date])
#     return data_list
#
#
# # 结构如下
# # {
# #   "code": 0,
# #   "msg": "success",
# #   "data": [
# #     {
# #       "stockCode": "399001",
# #       "cnName": "深证成指",
# #       "source": "sz",
# #       "areaCode": "cn",
# #       "market": "a",
# #       "publishDate": "1994-12-31T16:00:00.000Z"
# #     },
# #     {
# #       "stockCode": "399005",
# #       "cnName": "中小板指",
# #       "source": "sz",
# #       "areaCode": "cn",
# #       "market": "a",
# #       "publishDate": "2006-01-23T16:00:00.000Z"
# #     }
# #   ]
# # }
#
#
# def mydb_set_tc2ics():
#     # 删除旧数据
#     tc2ics = TC2IC.query.all()
#     for tc2ic in tc2ics:
#         db.session.delete(tc2ic)
#     db.session.commit()
#     funds_filters = {
#         Fund.fund_investtype == u'被动指数型基金',
#         Fund.fund_trackindexcode != ''
#     }
#     ft = Fund.fund_trackindexcode
#     # 万得的跟踪代码查询结果
#     tcs = Fund.query.filter(*funds_filters).with_entities(ft).group_by(ft).all()
#     # 万得跟踪代码带字母到不带字母的映射：{不带字母:带字母,...}
#     tcs_dict = {}
#     for tc in tcs:
#         tcs_dict.setdefault(tc[0].split('.')[0], tc[0])
#     sc = LXRIndice.stock_code
#     cn = LXRIndice.cn_name
#     # 理杏仁指数代码查询结果
#     ics = LXRIndice.query.with_entities(sc, cn).group_by(sc, cn).all()
#     # 带字母
#     track_code = []
#     # 不带字母
#     indice_code = []
#     # 指数简称
#     cn_name = []
#     # 当前值
#     latest_pe_ttm = []
#     # 当前分位点
#     latest_per = []
#     # 最大值
#     max_pe_ttm = []
#     # 最小值
#     min_pe_ttm = []
#     # 中位值
#     mid_pe_ttm = []
#     # 危险值
#     risk_pe_ttm = []
#     # 机会值
#     chance_pe_ttm = []
#     for ic in ics:
#         if ic[0] in tcs_dict:
#             tc2ic = TC2IC(
#                 track_code=tcs_dict[ic[0]],
#                 indice_code=ic[0],
#                 cn_name=ic[1]
#             )
#             db.session.add(tc2ic)
#     db.session.commit()
#
#
# if __name__ == '__main__':
#     with create_app('default').app_context():
#         pass
#         # mydb_init()
#         # mydb_set_tc2ics()

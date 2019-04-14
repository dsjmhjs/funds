import os
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_login import LoginManager
from flask_mail import Mail
from threading import Thread
from flask import render_template, current_app
from flask_mail import Message
from flask_pagedown import PageDown
from flask_ckeditor import CKEditor
# redis
from redis import StrictRedis

basedir = os.path.abspath(os.path.dirname(__file__))
bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()
mail = Mail()
pagedown = PageDown()
ckeditor = CKEditor()
rds = StrictRedis()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['MAIL_USERNAME'], recipients=[to])
    # msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


class Config:
    def __init__(self):
        pass

    SECRET_KEY = 'hard to guess string'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = '25'
    # read from environment variable
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '<Flaskyyy>'
    # FLASKY_MAIL_SENDER = 'km <451221245@qq.com>'
    FLASKY_BLOGS_PER_PAGE = 10
    FLASKY_FOLLOWERS_PER_PAGE = 10
    FLASKY_COMMENTS_PER_PAGE = 10

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123457@localhost:3306/xxxdb'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')


class TestingConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123457@localhost:3306/flaskyyydb_test'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    # 'production': ProductionConfig,
    'default': DevelopmentConfig
}

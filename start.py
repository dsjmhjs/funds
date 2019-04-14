from flask import Flask
from config import config
from config import db, bootstrap, moment, mail, login_manager, pagedown, ckeditor
from models.users import AnonymousUser


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    pagedown.init_app(app)
    ckeditor.init_app(app)
    login_manager.init_app(app)
    login_manager.anonymous_user = AnonymousUser

    from contrs.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from contrs.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app


capp = create_app('default')
if __name__ == '__main__':
    capp.run()

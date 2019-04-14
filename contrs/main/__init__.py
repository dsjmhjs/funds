# -*- coding: utf-8 -*-
from flask import Blueprint

main = Blueprint('main', __name__)

from contrs.main import main_contr, errors  # noqa
from models.roles import Perm  # noqa


# 在模板中可能也需要检查权限，上下文处理器
@main.app_context_processor
def inject_permissions():
    return dict(Perm=Perm)

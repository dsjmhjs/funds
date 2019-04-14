from flask import Blueprint

auth = Blueprint('auth', __name__)

from contrs.auth import auth_contr, errors  # noqa

from flask import render_template
from contrs.auth import auth


@auth.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@auth.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500

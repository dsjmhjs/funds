from flask import render_template
from contrs.main import main


@main.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@main.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500

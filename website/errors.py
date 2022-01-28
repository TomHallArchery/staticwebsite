from flask import Blueprint, render_template

errors_bp = Blueprint('errors', __name__)


@errors_bp.app_errorhandler(404)
def page_not_found(e):
    ''' return 404 status code and template '''
    print(e)
    return render_template('generic/404.html.j2'), 404

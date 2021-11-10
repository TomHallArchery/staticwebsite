from flask import current_app as app
from flask import render_template


def render_404():
    ''' return 404 page html template '''
    return render_template('generic/404.html.j2')


@app.errorhandler(404)
def page_not_found(e):
    ''' return 404 status code and template '''
    print(e)
    return render_404(), 404

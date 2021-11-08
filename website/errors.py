from website import app
from flask import render_template


def render_404():
    return render_template('generic/404.html.j2')


@app.errorhandler(404)
def page_not_found(e):
    return render_404(), 404

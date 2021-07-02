from website import app, flatpages
from flask import render_template

@app.errorhandler(404)
def page_not_found(e):
    return render_template('generic/404.html.j2'), 404

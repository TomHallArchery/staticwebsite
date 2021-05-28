from website import app, flatpages
import flask

@app.errorhandler(404)
def page_not_found(e):
    return flask.render_template('generic/404.html.j2'), 404

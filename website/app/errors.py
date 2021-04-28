from app import app
import flask

@app.errorhandler(404)
def page_not_found(e):
    return flask.render_template('base/404.j2'), 404

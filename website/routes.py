from datetime import datetime

import flask
from flask import current_app as app
from website import utils
from .images import services as img_services


@app.context_processor
def inject_data():
    ''' global context for all templates '''
    this_year = datetime.now().year
    return dict(
        year=this_year,
        img_sizes=app.config.get('IMG_WIDTHS'),
        img_layout=app.config.get('IMG_DISPLAY_WIDTHS'),
        sizes=img_services._write_sizes_attr,
        utils=utils,
        )


# ===============
# ROUTES
# ===============


@app.route('/')
def home_page():
    ''' render homepage '''
    return flask.render_template(
        'home.html.j2',
        title="Home",
        description="The homepage of Tom Hall, Archer and Coach",
        keywords="Archery, Athlete, Profile",
        img_layout={'min-width: 110ch': '60vw', None: '95vw'},
        )


@app.route("/test/")
def serve_test():
    ''' render test page '''
    print("TESTVAR: ", app.config["VIEW_TEST"])
    if not app.config["VIEW_TEST"]:
        flask.abort(404)
    return flask.render_template('generic/test.html.j2')

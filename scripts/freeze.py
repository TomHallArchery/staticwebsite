#!/usr/bin/env python
import os

import flask
from flask_htmlmin import HTMLMIN
from flask_frozen import Freezer

from website import create_app, utils
import config

# configure app for freezing locally or for deployment
conf = os.environ.get("APP_CONFIG")
if conf == "Deploy":
    app = create_app(config.DeployConfig)
else:
    app = create_app(config.BuildConfig)

HTMLMIN(app)
freezer = Freezer(app)


# Instructs the freezer to also check for dynamically generated urls
# from serve_page functinon.
@freezer.register_generator
def register_fonts():
    ''' Register font files with frozen flask '''
    fonts = app.config["FONTS"]
    for path, font in fonts.items():
        file = os.path.join('fonts', path, font)
        yield flask.url_for('static', filename=file)


def main():
    ''' Freeze website into static files '''
    print("Building website:")

    # TODO: check font files exist and compile with pyftsubset

    # Freeze static files into default directory 'build'
    freezer.freeze()
    print("Website frozen")

    with app.app_context():
        utils.compile_css(compressed=True)
        print("Css recompiled")

    # Frozen flask issue:
    # have to manually build the 404 error page for use by server
    with app.test_request_context():
        error_page = flask.render_template('generic/404.html.j2')
        with open('website/build/404.html', 'w', encoding="utf-8") as f:
            f.write(error_page)


if __name__ == '__main__':
    main()

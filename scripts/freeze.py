#!/usr/bin/env python
import os
from flask_frozen import Freezer
from flask import url_for, render_template

from website import app, flatpages, utils, images, errors
import config

conf = os.environ.get("APP_CONFIG")
if conf == "Deploy":
    app.config.from_object(config.DeployConfig)
else:
    app.config.from_object(config.BuildConfig)

freezer = Freezer(app)

FONTS = app.config["FONTS"]
BUILD_PATH = "website/build"

# Instructs the freezer to also check for dynamically generated urls from serve_page functinon.
@freezer.register_generator
def fonts():
    for dir, font in FONTS.items():
        path = os.path.join('fonts', dir, font)
        yield url_for('static', filename=path)

#Frozen flask issue: have to manually build the 404 error page for use by server
def build_404():
    with app.test_request_context():
        error_page = errors.render_404()
        with open('website/build/404.html', 'w') as f:
            f.write(error_page)

def main():
    print("Building website:")

    # TODO: check font files exist and compile with pyftsubset
    build_404()
    # Freeze static files into default directory 'build'
    freezer.freeze()
    print("Website frozen")

    utils.compile_css(compressed=True)
    print("Css recompiled")

if __name__ == '__main__':
    main()

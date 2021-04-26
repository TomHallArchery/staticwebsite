#!/usr/bin/env python

from app import app, flatpages
from flask_frozen import Freezer
from flask import url_for

freezer = Freezer(app)

# Instructs the freezer to also check for dynamically generated urls
# from serve_page functinon.
@freezer.register_generator
def pagelist():
    for page in flatpages:
        yield url_for('serve_page', path_requested=page.path)

if __name__ == '__main__':
    freezer.freeze()

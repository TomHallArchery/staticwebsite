#!/usr/bin/env python

from app import app, flatpages
from flask_frozen import Freezer
from flask import url_for
import http.server as svr
import os

freezer = Freezer(app)

# Instructs the freezer to also check for dynamically generated urls
# from serve_page functinon.
@freezer.register_generator
def pagelist():
    for page in flatpages:
        yield url_for('serve_page', path_requested=page.path)

if __name__ == '__main__':
    # Freeze static files into default directory 'build'
    freezer.freeze()
    # Use python builtin server to serve static files based on directory structure
    os.chdir('build')
    svr.test(HandlerClass=svr.SimpleHTTPRequestHandler)

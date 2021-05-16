#!/usr/bin/env python

from website import app, flatpages
from flask_frozen import Freezer
from flask import url_for
import http.server as svr
import os
import subprocess

freezer = Freezer(app)

# Instructs the freezer to also check for dynamically generated urls from serve_page functinon.
# @freezer.register_generator
# def pagelist():
#     # limit to articles
#     for page in flatpages:
#         yield url_for('serve_article', path_requested=page.path)

if __name__ == '__main__':
    # Freeze static files into default directory 'build'
    freezer.freeze()
    print("Website frozen")
    # cmnd = "python -m pynetlify deploy_folder --site-id bd867c99-8ad2-41da-b295-d619581e8079 website/static/img/"
    # res = subprocess.call(cmnd, shell = True)
    # print("Pynetlify deploy folder exit code: ", res)
    # Use python builtin server to serve static files based on directory structure
    os.chdir('website/build')
    svr.test(HandlerClass=svr.SimpleHTTPRequestHandler, port=5001)

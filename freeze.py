#!/usr/bin/env python

from website import app, flatpages
from website.utils import compile_css, cwd
from website.images import hash_dir_filenames, upload_images
from webssite.errors import render_404
from flask_frozen import Freezer
from flask import url_for, render_template
import http.server as svr
import os

freezer = Freezer(app)
app.config["FREEZER_DESTINATION_IGNORE"] += ['404.html', '_headers']
app.config["FREEZER_STATIC_IGNORE"] += ['fonts/', 'scss/', 'img/', 'css/', 'favicon/', 'js/']

# Manually add fonts to list to incorporate into freezer
FONTS = {
'Roboto_Slab' : 'RobotoSlab-VariableFont_wght-Latin.woff2', #tuple: vf, latin, woff2
'Public_Sans' : 'PublicSans-VariableFont_wght-Min.woff2'
}
IMAGES_URL = "https://cdn.tomhallarchery.com/"

# Instructs the freezer to also check for dynamically generated urls from serve_page functinon.
@freezer.register_generator
def fonts():
    print('Registering Font files:')
    for dir, font in FONTS.items():
        path = os.path.join('fonts', dir, font)
        print(path)
        yield url_for('static', filename=path)

#Frozen flask issue: have to manually build the 404 error page for use by server
def build_404():
    with app.test_request_context():
        error_page = render_404()
        with open('website/build/404.html', 'w') as f:
            f.write(error_page)



def main():
    print("Building website:")
    # print(app.config)
    # TODO: check font files exist and compile with pyftsubset
    build_404()
    # Freeze static files into default directory 'build'
    freezer.freeze()
    print("Website frozen")

    compile_css('website/static/scss', 'website/build/static/css', compressed=True)
    print("Css recompiled")

    # Deploy static images output to seperate netlify repo
    # Automated deploy if any filenames change (not file contents!)
    if hash_dir_filenames('website/static/img/out', 'hash.txt'):
        print('Uploading images:')
        upload_images('website/static/img/out')
        print('DONE')
    else:
        print('No new images to upload')

    # Use python builtin server to serve static files based on directory structure
    with cwd('website/build'):
        svr.test(HandlerClass=svr.SimpleHTTPRequestHandler, port=5001)




if __name__ == '__main__':

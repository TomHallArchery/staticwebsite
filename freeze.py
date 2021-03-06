#!/usr/bin/env python

from website import app, flatpages, utils, images, errors

from flask_frozen import Freezer
from flask import url_for, render_template

import os
import argparse

freezer = Freezer(app)
app.config["FREEZER_DESTINATION_IGNORE"] += ['404.html', '_headers']
app.config["FREEZER_STATIC_IGNORE"] += ['fonts/', 'scss/', 'img/', 'css/', 'favicon/', 'js/']

# Manually add fonts to list to incorporate into freezer
FONTS = {
'Roboto_Slab' : 'RobotoSlab-VariableFont_wght-Latin.woff2', #tuple: vf, latin, woff2
'Public_Sans' : 'PublicSans-VariableFont_wght-Min.woff2'
}
IMAGES_URL = "https://cdn.tomhallarchery.com/"
BUILD_PATH = "website/build"

# Instructs the freezer to also check for dynamically generated urls from serve_page functinon.
@freezer.register_generator
def fonts():
    print('Registering Font files:')
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
    parser = argparse.ArgumentParser(description="Freeze website into static files")
    parser.add_argument('-S', '--serve', action='store_true',
        help="Serve built files on port 5001")
    args = parser.parse_args()

    print("Building website:")
    # print(app.config)
    # TODO: check font files exist and compile with pyftsubset
    build_404()
    # Freeze static files into default directory 'build'
    freezer.freeze()
    print("Website frozen")

    utils.compile_css('website/static/scss', 'website/build/static/css', compressed=True)
    print("Css recompiled")

    # Deploy static images output to seperate netlify repo
    # Automated deploy if any filenames change (not file contents!)
    if images.hash_dir_filenames('website/static/img/out', 'hash.txt'):
        print('Uploading images:')
        images.upload_images('website/static/img/out')
        print('DONE')
    else:
        print('No new images to upload')

    # Use python builtin server to serve static files based on directory structure
    if args.serve:
        utils.serve_static('website/build', 5001)


if __name__ == '__main__':
    main()

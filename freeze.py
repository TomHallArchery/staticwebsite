#!/usr/bin/env python

from website import app, flatpages
from flask_frozen import Freezer
from flask import url_for
import http.server as svr
import os
import subprocess
import hashlib

freezer = Freezer(app)

# Manually add fonts to list to incorporate into freezer
FONTS = {
'Roboto_Slab' : 'RobotoSlab-VariableFont_wght-Latin.woff2', #tuple: vf, latin, woff2
'Public_Sans' : 'PublicSans-VariableFont_wght-Min.woff2'
}

IMG_DIR = 'website/static/img/out'

# Instructs the freezer to also check for dynamically generated urls from serve_page functinon.
@freezer.register_generator
def fonts():
    for dir, font in FONTS.items():
        path = os.path.join('fonts', dir, font)
        print(path)
        yield url_for('static', filename=path)

def hash_dir_filenames(dir, hashfile):
    ''' Calculates hash of sorted list of files in directory and writes it to hashfile, return True for change in hash '''
    # Deploy static images output to seperate netlify repo
    # Automated deploy if any filenames change (not file contents!)
    try:
        owd = os.getcwd()
        os.chdir(dir)
        dirlist = ",".join(sorted(os.listdir()))
        new_hash = hashlib.sha256(dirlist.encode()).hexdigest()

        with open(hashfile, "r") as f:
            old_hash = f.read()

        with open(hashfile, "w") as f:
            f.write(new_hash)

    finally:
        os.chdir(owd)

    return new_hash != old_hash

# eg hash_dir_filenames('website/static/img/out', 'hash.txt')

def upload_images(dir):
    cmnd = ['python', '-m', 'pynetlify', 'deploy_folder', '--site-id', 'bd867c99-8ad2-41da-b295-d619581e8079', dir]
    res = subprocess.run(cmnd)
    print(res)
    print("Uploaded files:")
    for file in sorted(os.listdir('website/static/img/out')):
        print(file)

def compile_css(src, dest):
    cmnd = ["sass", f"{src}:{dest}", "--no-source-map"]
    res = subprocess.run(cmnd)

if __name__ == '__main__':
    print("Building website:")

    # TODO: compile scss with sass commandline: here or in run?
    # TODO: check font files exist and compile with pyftsubset

    # Freeze static files into default directory 'build'
    freezer.freeze()
    print("Website frozen")

    # If dir hash has changed, upload images:
    if hash_dir_filenames(IMG_DIR, 'hash.txt'):
        upload_images(IMG_DIR)


    # Use python builtin server to serve static files based on directory structure
    os.chdir('website/build')
    svr.test(HandlerClass=svr.SimpleHTTPRequestHandler, port=5001)

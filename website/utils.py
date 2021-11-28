import subprocess
import os
from contextlib import contextmanager

from pynetlify import pynetlify
from bs4 import BeautifulSoup

from flask import current_app as app
from website import flatpages


@contextmanager
def cwd(path):
    oldpwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(oldpwd)


def rm_file(file):
    ''' Remove file at path without exceptions for not found or directory '''
    if os.path.exists(file) and os.path.isfile(file):
        os.remove(file)


def compile_css(app, compressed=False, watch=False):
    ''' launch subprocess to run dart sass '''
    source = app.config["CSS_SRC_DIR"]
    dest = app.config["CSS_OUT_DIR"]
    cmnd = ["sass", f"{source}:{dest}", "--no-source-map"]
    if compressed:
        cmnd.extend(["-s", "compressed"])
    if watch:
        cmnd.extend(['--watch'])
    res = subprocess.Popen(cmnd)
    return res


# dirty:
# strip '---' from ._meta attribute of page objects
# to allow flatpages to work with yaml delimiter
def clean_flatpage_metas(pages):
    ''' strip "---" from all flatpage objects in pages '''
    for page in pages:
        page._meta = page._meta.strip('---')


# add filtering method to flatpages object
def filter_pages(path):
    ''' return list of flask flatpage objects from subdirectory of "pages" '''
    return list(
        page for page in flatpages
        if os.path.dirname(page.path) == path
        )


def parse_html(html):
    ''' wrapper for initialising an HTML Parser'''
    return BeautifulSoup(html, 'html.parser')


def split_filename(path):
    ''' return path, filename and extension from a path like string '''
    path, file = os.path.split(path)
    fname, ext = os.path.splitext(file)
    return (path, fname, ext)


def src(imgs_domain, img_path):
    ''' return image src attribute from prefix url and file name'''
    return os.path.join(imgs_domain, img_path)


def srcset(imgs_domain, fname, widths, ext):
    ''' return image srcset attribute for set img widths'''
    srcset_list = (
        f'{src(imgs_domain, fname)}_{width}.{ext} {width}w'
        for width in widths
        )
    return ", ".join(srcset_list)


def sizes(criteria):
    ''' usage: sizes({'60vw':'min-width: 110ch', '95vw': None}) '''
    sizes_list = (f'({sz}) {br}' for sz, br in criteria.items())
    return ", ".join(sizes_list).replace('(None) ', '')


def deploy_folder_to_netlify(directory, subdomain):
    ''' deploys specified directory contents via pynetlify '''
    subdomain = subdomain.upper()
    assert subdomain in ['ROOT', 'CDN']

    auth_token = app.config.get('NETLIFY_AUTH_TOKEN')
    domain_id = app.config.get(f'NETLIFY_{subdomain}_ID')

    netlify = pynetlify.APIRequest(auth_token)
    target = netlify.get_site(domain_id)
    return netlify.deploy_folder_to_site(directory, target)


def main():
    '''  '''
    pass


if __name__ == '__main__':
    main()

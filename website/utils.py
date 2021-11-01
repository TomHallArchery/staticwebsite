import subprocess
import os
import AdvancedHTMLParser
import http.server as svr
from contextlib import contextmanager
from pynetlify import pynetlify

from website import app, flatpages

@contextmanager
def cwd(path):
    oldpwd=os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(oldpwd)

def rm_file(file):
    ''' Remove file at path without exceptions for not found or directory '''
    if os.path.exists(file) and os.path.isfile(file):
        os.remove(file)

def compile_css(src, dest, compressed=False, watch=False):
    cmnd = ["sass", f"{src}:{dest}", "--no-source-map"]
    if compressed:
        cmnd.extend([ "-s", "compressed"])
    if watch:
        cmnd.extend(['--watch'])
    res = subprocess.run(cmnd)
    return res

# dirty:
# strip '---' from ._meta attribute of page objects to allow flatpages to work with yaml delimiter
def clean_flatpage_metas(flatpages):
    for page in flatpages:
        page._meta = page._meta.strip('---')

# add filtering method to flatpages object
def filter_pages(path):
    ''' return list of flask flatpage objects from subdirectory of "pages" '''
    return list(page for page in flatpages if os.path.dirname(page.path) == path)


def parse_html(html):
    parser = AdvancedHTMLParser.AdvancedHTMLParser()
    parser.parseStr(html)
    return parser

def split_filename(input):
    path, file = os.path.split(input)
    fname, ext = os.path.splitext(file)
    return (path, fname, ext)

def src(img_url, fname):
    return os.path.join(img_url, fname)

def srcset(img_url, fname, widths, ext):
    srcset = [f'{img_url + fname}_{width}.{ext} {width}w' for width in widths]
    return ", ".join(srcset)

def sizes(criteria):
    ''' usage: sizes({'60vw':'min-width: 110ch', '95vw': None}) '''

    sizes = [f'({sz}) {br}' for sz, br in criteria.items()]
    return ", ".join(sizes).replace('(None) ', '')

def gen_img_attributes(src, img_url, fname, widths, ext, default_size, default_layout , height, width):
    path, fname, ext = split_filename(src)
    return [
        img_url + os.path.join(img_url, f'{fname}_{default_size}{ext}'),
        srcset(img_url, fname, sizes, ext),
        sizes(default_layout),
        height,
        width
    ]

def serve_static(dir, port):
    with cwd(dir):
        svr.test(HandlerClass=svr.SimpleHTTPRequestHandler, port=port)

def deploy_folder_to_netlify(dir, subdomain):
    subdomain = subdomain.upper()
    assert subdomain in ['ROOT', 'CDN']

    AUTH_TOKEN = app.config.get('NETLIFY_AUTH_TOKEN')
    DOMAIN_ID = app.config.get(f'NETLIFY_{subdomain}_ID')

    netlify = pynetlify.APIRequest(AUTH_TOKEN)
    target = netlify.get_site(DOMAIN_ID)
    return netlify.deploy_folder_to_site(dir, target)


def main():
    return

if __name__ == '__main__':
    main()

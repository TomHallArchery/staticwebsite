import subprocess
import os
from contextlib import contextmanager

from pynetlify import pynetlify
from bs4 import BeautifulSoup


@contextmanager
def cwd(path):
    oldpwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(oldpwd)


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


def deploy_folder_to_netlify(app, directory, subdomain):
    ''' deploys specified directory contents via pynetlify '''
    subdomain = subdomain.upper()
    assert subdomain in ['ROOT', 'CDN']

    auth_token = app.config.get('NETLIFY_AUTH_TOKEN')
    domain_id = app.config.get(f'NETLIFY_{subdomain}_ID')

    netlify = pynetlify.APIRequest(auth_token)
    target = netlify.get_site(domain_id)
    return netlify.deploy_folder_to_site(directory, target)

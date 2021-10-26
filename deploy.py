import os
from pynetlify import pynetlify

from website import app

def netlify_deploy():
    netlify = pynetlify.APIRequest(os.environ.get('NETLIFY_AUTH_TOKEN'))
    target = netlify.get_site(os.environ.get('ROOT_NETLIFY_ID'))
    return netlify.deploy_folder_to_site("website/build", target)

if __name__ == '__main__':
    netlify_deploy()

from pynetlify import pynetlify

import config
from website import create_app

from . import cli_bp as bp


def deploy_folder_to_netlify(app, directory, subdomain):
    ''' deploys specified directory contents via pynetlify '''
    subdomain = subdomain.upper()
    assert subdomain in ['ROOT', 'CDN']

    auth_token = app.config.get('NETLIFY_AUTH_TOKEN')
    domain_id = app.config.get(f'NETLIFY_{subdomain}_ID')

    netlify = pynetlify.APIRequest(auth_token)
    target = netlify.get_site(domain_id)
    return netlify.deploy_folder_to_site(directory, target)


@bp.cli.command('deploy')
def main():
    """ Deploy application to netlify """
    app = create_app(config.DeployConfig)

    deploy_folder_to_netlify(app, 'website/build', "ROOT")
    deploy_folder_to_netlify(app, 'website/static/img/out', "CDN")

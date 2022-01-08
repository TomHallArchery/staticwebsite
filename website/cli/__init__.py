from pprint import pformat

import click
from flask import Blueprint

cli_bp = Blueprint('cli', __name__, cli_group=None)

from . import deploy, develop, freeze, serve, vendorize  # noqa


@cli_bp.cli.command('config')
def show_config():
    """ Show current app config for default app in wsgi.py """

    from flask import current_app
    click.echo('App Config: ')
    click.echo_via_pager(pformat(current_app.config))


# TODO: dev command
# TODO: build(staging) command
# TODO: deploy command
# TODO: testing command & testing code
# TODO: absorb vendorizing into build?
# TODO: remove process images script (have img bp commands)
# TODO: font processing

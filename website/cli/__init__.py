import click
from flask import Blueprint

cli_bp = Blueprint('cli', __name__, cli_group=None)


@cli_bp.cli.command('test-cli')
def test_bp():
    click.echo('Testing:')
    click.echo(cli_bp.import_name)

# TODO: dev command
# TODO: build(staging) command
# TODO: deploy command
# TODO: testing command & testing code
# TODO: absorb vendorizing into build?
# TODO: remove process images script (have img bp commands)
# TODO: font processing

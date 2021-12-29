import click
from flask import Blueprint

cli_bp = Blueprint('cli', __name__, cli_group=None)


@cli_bp.cli.command('test')
def test_bp():
    click.echo('Testing:')
    click.echo(cli_bp.import_name)

import click

from . import pages_bp as bp
from . import services as sv


@bp.cli.command('create')
@click.argument('name')
def create_page(name):
    sv.create_page(name)


@bp.cli.command('delete')
@click.argument('name')
def delete_page(name):
    sv.delete_page(name)


@bp.cli.command('read')
@click.argument('name')
def read_page(name):
    sv.read_page(name)


@bp.cli.command('init')
def init_db():
    sv.init_db_from_files()

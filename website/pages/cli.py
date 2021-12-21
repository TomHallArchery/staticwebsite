import click

from . import pages_bp as bp
from . import services as sv


@bp.cli.command('select')
@click.argument('name')
def select_page(name):
    return sv.select_page_by_name(name)


@bp.cli.command('create')
@click.argument('name')
@click.option('-i', '--interactive', is_flag=True)
def create_page(name, interactive):
    page = sv.create_page(name)
    if interactive:
        page.metadata.title = click.prompt('Page title')
        page.metadata.description = click.prompt('Page description')


@bp.cli.command('delete')
@click.argument('name')
def delete_page(name):
    sv.delete_page(name)


@bp.cli.command('pull')
@click.argument('name')
def pull_metadata(name):
    page = sv.select_page_by_name(name)
    metadata = page.pull_from_file()
    click.echo(repr(page))
    click.echo(metadata)


@bp.cli.command('push')
@click.argument('name')
def push_metadata(name):
    page = sv.select_page_by_name(name)
    metadata = page.push_to_file()
    click.echo(repr(page))
    click.echo(metadata)


@bp.cli.command('init')
def init_collection():
    sv.init_db_from_files()


@bp.cli.command('drop')
def drop_collection():
    sv.drop_collection()

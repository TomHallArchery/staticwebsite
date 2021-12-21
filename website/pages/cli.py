import click
from time import sleep

from . import pages_bp as bp
from . import services as sv


@bp.cli.command('select')
@click.argument('name')
def select_page(name):
    page = sv.select_page_by_name(name)
    click.echo(repr(page))


@bp.cli.command('list')
def list_pages():
    for page in sv.select_all_pages():
        click.echo(f"{page.status.name:12}{page.name:24}")


@bp.cli.command('create')
@click.argument('name')
@click.option('-i', '--interactive', is_flag=True)
@click.option('--edit/--no-edit', default=True)
def create_page(name, interactive, edit):
    page = sv.create_page(name)
    if interactive:
        page.metadata.title = click.prompt('Page title')
        page.metadata.description = click.prompt('Page description')
        page.metadata.keywords = click.prompt('Page keywords')
        page.push_to_file()
    if edit:
        sleep(1)
        click.launch(page.filepath)


@bp.cli.command('delete')
@click.argument('names', nargs=-1)
def delete_pages(names):
    sv.delete_pages(names)


@bp.cli.command('edit')
@click.argument('name')
def edit_page(name):
    page = sv.select_page_by_name(name)
    click.launch(page.filepath)


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


@bp.cli.command('push-all')
def push_all_metadata():
    for page in sv.select_all_pages():
        page.push_to_file()


@bp.cli.command('publish')
@click.argument('name')
def publish_page(name):
    page = sv.select_page_by_name(name)
    click.echo(f"{page!r}")
    if click.confirm('Publish Page?'):
        sv.publish_page(page)
        click.echo("Page Published")


@bp.cli.command('init')
def init_collection():
    sv.init_db_from_files()


@bp.cli.command('drop')
@click.confirmation_option(prompt='Drop pages collection?')
def drop_collection():
    sv.drop_collection()

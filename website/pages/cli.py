import click

from . import pages_bp as bp
from .models import Page, Pages


@bp.cli.command('create')
@click.argument('name')
def create_page(name):
    page = Page(name=name)
    page.filepath = f'website/content/{name}.md'
    page.path.touch()
    page.save()


@bp.cli.command('delete')
@click.argument('name')
def delete_page(name):
    pages = Pages.query(name=name)
    for page in pages:
        page.path.unlink()
        page.delete()

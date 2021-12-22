import click
from pathlib import Path

from . import images_bp as bp
from . import services as sv
from .models import Img

IMG_SRC_DIR = Path(sv.IMAGES_ROOT, sv.SOURCE_DIR)


@bp.cli.command('select')
@click.argument('path', type=click.Path(exists=True))
def select_img(path):
    img = Img.objects.get(filepath=path)
    click.echo(img)


@bp.cli.command('list')
def list_imgs():
    for img in Img.objects:
        click.echo(
            f"{img.status.name:12}{img.name:40}"
            f"{img.thumbnail_widths}"
        )


@bp.cli.command('view')
@click.argument('fn', type=click.Path(exists=True))
def view_img(fn):
    click.launch(fn)


def complete_img_names(ctx, param, incomplete):
    return [
        str(fn) for fn in IMG_SRC_DIR.iterdir()
        if fn.stem.startswith(incomplete)
        ]


@bp.cli.command('process')
@click.argument('name', shell_complete=complete_img_names)
def process_img(name):
    img = Img.objects.get(name=name)
    sv.process_img(img)

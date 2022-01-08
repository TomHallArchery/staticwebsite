import itertools
import shutil
from pathlib import Path

import click

from . import images_bp as bp
from . import services as sv
from .models import Image

IMG_SRC_DIR = Path(sv.IMAGES_ROOT, sv.SOURCE_DIR)
IMG_OUT_DIR = Path(sv.IMAGES_ROOT, sv.OUTPUT_DIR)

bp.cli.short_help = "SUBCOMMAND Images command group"

# callbacks
def find_by_name_or_file(ctx, param, name_or_file):
    if not name_or_file:
        return None
    path = Path(name_or_file)

    # use filename to lookup on images directory
    if path.parent == Path('.'):
        search = itertools.chain(
            IMG_SRC_DIR.iterdir(),
            IMG_OUT_DIR.iterdir(),
        )
        # try SOURCE_DIR first
        for fn in search:
            if fn.name == path.name:
                return fn

    # return filename directly
    else:
        return path


path_arg = click.argument(
    'path',
    callback=find_by_name_or_file,
    required=False,
)


@bp.cli.command('list')
def list_imgs():
    for image in Image.objects:
        click.echo(
            f"{image.status.name:12}{image.name:40}"
            f"{image.thumbnail_widths}"
        )


@bp.cli.command('view')
@path_arg
def view_img(path):
    ''' View source img at PATH '''
    fn = str(path)
    click.echo(fn)
    click.launch(fn)


@bp.cli.command('add')
@click.option('-c', '--copy/--no-copy', default=True)
@path_arg
def add_img(path, copy):
    if copy:
        path = shutil.copy(path, IMG_SRC_DIR / path.name)

    sv.add_img_to_db(path)


@bp.cli.command('delete')
@path_arg
def delete_img(path):
    click.echo(path)
    click.confirm(f'Delete image {path} ?', abort=True)
    images = Image.objects(filepath=str(path))
    sv.delete_images(images)


@bp.cli.command('process')
@click.option('-a', '--all', 'process_all', is_flag=True)
@path_arg
def process_img(path, process_all):
    if process_all:
        for image in Image.objects:
            sv.process_img(image)
            click.echo(image.name)
        return

    image = Image.objects.get(name=path.name)
    sv.process_img(image)


@bp.cli.command('test-compression')
@path_arg
def test_img_compression(path):
    image = Image.objects.get(filepath=str(path))
    test = sv.test_compression(image)
    click.echo(test)


# @bp.cli.command('looping')
# @click.option('--io/--no-io', 'with_io')
# def test(with_io):
#     if with_io:
#         for image in Image.objects:
#             sv.pil_open_img(image)
#             for width in image.thumbnail_widths:
#                 for format in image.formats:
#                     click.echo(format.outputs)
#     else:
#         for image in Image.objects:
#             for width in image.thumbnail_widths:
#                 for format in image.formats:
#                     click.echo(format.outputs)


@bp.cli.command('init')
def init_images_collection():
    sv.init_db_from_files()


@bp.cli.command('drop')
@click.confirmation_option(prompt='Drop images collection?')
def drop_images_collection():
    Image.drop_collection()

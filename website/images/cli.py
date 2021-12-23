from pathlib import Path
import shutil

import click

from . import images_bp as bp
from . import services as sv
from .models import Image

IMG_SRC_DIR = Path(sv.IMAGES_ROOT, sv.SOURCE_DIR)
IMG_OUT_DIR = Path(sv.IMAGES_ROOT, sv.OUTPUT_DIR)


# callbacks
def find_by_name_or_file(ctx, param, name_or_file):
    path = Path(name_or_file)

    # use filename to lookup on images directory
    if path.parent == Path('.'):

        # try SOURCE_DIR first
        for fn in IMG_SRC_DIR.iterdir():
            if fn.name == path.name:
                return fn

        for fn in IMG_OUT_DIR.iterdir():
            if fn.name == path.name:
                return fn
    # return filename directly
    else:
        return path


path_arg = click.argument(
    'path',
    callback=find_by_name_or_file
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
@click.option('-s', '--skip/--no-skip', 'skip_processed', default=True)
@click.option('-a', '--all', 'process_all', is_flag=True)
@path_arg
def process_img(file, name, process_all, skip_processed):
    if process_all:
        for image in Image.objects:
            sv.process_img(image, skip_processed)
            click.echo(image.name)
        return

    name = name or file.name
    image = Image.objects.get(name=name)
    sv.process_img(image)


@bp.cli.command('init')
def init_images_collection():
    sv.add_all_imgs_to_db()


@bp.cli.command('drop')
@click.confirmation_option(prompt='Drop images collection?')
def drop_images_collection():
    sv.drop_collection()

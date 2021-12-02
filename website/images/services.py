from pathlib import Path
from typing import Any, Iterator
import os

import PIL.Image
import PIL.ImageOps
import bs4
from flask import current_app
from mongoengine.errors import NotUniqueError

from .models import Img
from config import Config

# Constants
# Only appear in base config
IMAGES_ROOT = Config.IMG_ROOT
SOURCE_DIR = Config.IMG_SOURCE_DIR
OUTPUT_DIR = Config.IMG_OUTPUT_DIR


def add_all_imgs_to_db() -> None:
    '''
    Creates Img model from all image files in source directory

    Used to instantiate database from scratch
    '''
    img_path = Path(IMAGES_ROOT, SOURCE_DIR)
    for path in img_path.iterdir():
        i = Img(name=path.name, type=path.suffix, filepath=str(path))
        try:
            i.save()
            print(f"[Saved] Img: {i.name} to db")
        except NotUniqueError:
            print(f"[Skipped] Img: {i.name} already in db")
            continue


def process_img(image: Img) -> None:
    ''' save thumbnails and update img database '''
    if image.status == image.status.PROCESSED:
        return
    sizes = _create_thumbnails(image)
    image.update(**sizes)
    image.update(status=image.status.PROCESSED)


def _write_src(img_path: str) -> str:
    ''' return image src attribute from prefix url and file name'''
    return current_app.config["IMG_URL"] + img_path


def _write_srcset(path: Path, widths: list[int]) -> str:
    ''' return image srcset attribute for set img widths'''
    srcset_list = (
        f'{_write_src(path.stem)}_{width}{path.suffix} {width}w'
        for width in widths
        )
    return ", ".join(srcset_list)


def _set_img_tag(
        img: bs4.element.Tag,
        model: Img
        ) -> None:
    path = model.path

    largest_src = _write_src(
        f"{path.stem}_{str(model.thumbnail_widths[0])}"
        f"{path.suffix}"
        )

    img.attrs.update({  # type: ignore[attr-defined]
        'src': largest_src,
        'srcset': _write_srcset(
            path,
            model.thumbnail_widths,
            ),
        'height': model.height,
        'width': model.width,
    })


def _wrap_picture(
        soup: bs4.BeautifulSoup,
        img: bs4.element.Tag,
        model: Img
        ) -> bs4.element.Tag:

    picture = soup.new_tag('picture')
    source = soup.new_tag('source')
    picture['class'] = img.get('class') or ""
    img['class'] = []
    img.wrap(picture)
    img.insert_before(source)

    source.attrs.update({  # type: ignore[attr-defined]
        'type': 'image/webp',
        'srcset': _write_srcset(
            model.path.with_suffix('.webp'),
            model.thumbnail_widths,
            ),
        'sizes': img.get('sizes', '')  # type: ignore[dict-item]
    })
    return picture


def responsive_images(html: str) -> str:
    ''' filter function for jinja templates

    returns html for responsive image syntax
    '''
    soup = bs4.BeautifulSoup(html, 'html.parser')
    imgs = soup.select('img[data-responsive]')

    for img in imgs:

        # Check prequistes met:
        # 1) img has a src attribute
        src = img.get('src')
        # 2) img is logged as processed in database
        model = Img.objects.get(name=src)

        if not src or model.status != model.status.PROCESSED:
            continue

        _set_img_tag(img, model)

        if 'no-wrap' not in img['data-responsive']:
            _wrap_picture(soup, img, model)

    return soup.prettify()


def _create_thumbnails(
        image: Img,
        ) -> dict[str, Any]:
    """ Generate and save thumbnails of given source image"""
    # open image in PIL
    pil = PIL.ImageOps.exif_transpose(PIL.Image.open(image.filepath))
    out = Path(IMAGES_ROOT, OUTPUT_DIR)

    widths = list(_select_thumbnail_widths(
        pil.width, pil.height, Config.IMG_WIDTHS
        ))

    for w in widths:
        thumb = pil.copy()
        thumb.thumbnail((w, pil.height), resample=PIL.Image.LANCZOS)
        thumb.save(
            f'{out}/{image.path.stem}_{w}.jpg',
            quality=55, optimize=True, progressive=True
            )
        thumb.save(
            f'{out}/{image.path.stem}_{w}.webp',
            quality=55, method=6
            )
    return dict(
        height=pil.width,
        width=pil.height,
        thumbnail_widths=widths,
    )


def _select_thumbnail_widths(
        width: int,
        height: int,
        standard_widths: list[int]
        ) -> Iterator[int]:
    '''
    returns widths of output images
    '''
    # filter standard widths down
    # to just those smaller than original image dimensions
    sizes = (x for x in standard_widths if max(width, height) > x)

    # correct width descriptor for portrait images
    widths = (min(s, s * width // height) for s in sizes)
    return widths


def src(imgs_domain, img_path):
    ''' return image src attribute from prefix url and file name'''
    return os.path.join(imgs_domain, img_path)


def srcset(imgs_domain, fname, widths, ext):
    ''' return image srcset attribute for set img widths'''
    srcset_list = (
        f'{src(imgs_domain, fname)}_{width}.{ext} {width}w'
        for width in widths
        )
    return ", ".join(srcset_list)


def sizes(criteria):
    ''' usage: sizes({'60vw':'min-width: 110ch', '95vw': None}) '''
    sizes_list = (f'({sz}) {br}' for sz, br in criteria.items())
    return ", ".join(sizes_list).replace('(None) ', '')

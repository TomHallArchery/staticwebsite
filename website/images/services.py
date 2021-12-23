from pathlib import Path
from typing import Any, Iterator
from collections import Iterable

import PIL.Image
import PIL.ImageOps
import bs4
from flask import current_app
from mongoengine.errors import NotUniqueError

from .models import Image
from config import Config

# Constants
# Only appear in base config
IMAGES_ROOT = Config.IMG_ROOT
SOURCE_DIR = Config.IMG_SOURCE_DIR
OUTPUT_DIR = Config.IMG_OUTPUT_DIR


def add_all_imgs_to_db() -> None:
    '''
    Creates Image model from all image files in source directory

    Used to instantiate database from scratch
    '''
    img_path = Path(IMAGES_ROOT, SOURCE_DIR)
    for path in img_path.iterdir():
        add_img_to_db(path)


def add_img_to_db(path) -> None:
    image = Image(name=path.name, type=path.suffix, filepath=str(path))
    try:
        image.save()
        print(f"[Saved] Image: {image.name} to db")
    except NotUniqueError:
        print(f"[Skipped] Image: {image.name} already in db")
        pass


def delete_images(images: Iterable[Image]) -> None:
    for image in images:
        image.path.unlink()
        image.delete()
    print(len(images))


def drop_collection() -> None:
    Image.drop_collection()


def process_img(image: Image, skip_processed: bool = True) -> None:
    ''' save thumbnails and update img database '''
    if skip_processed and image.status == image.status.PROCESSED:
        return
    sizes = _create_thumbnails(image)
    image.update(**sizes)
    image.update(status=image.status.PROCESSED)


def set_img_compression(image: Image, format: str, quality: int) -> int:
    image
    return quality


def _write_src(url_prefix: str, path: Path, width: int) -> str:
    ''' return image src attribute from prefix url and file name'''

    url = Path(url_prefix) / path.with_stem(f"{path.stem}_{width}").name
    return str(url)


def _write_srcset(url_prefix: str, path: Path, widths: Iterable[int]) -> str:
    ''' return image srcset attribute for set img widths'''

    srcset = (
        f'{_write_src(url_prefix, path, width)} {width}w'
        for width in widths
        )
    return ", ".join(srcset)


def _write_sizes(criteria: dict) -> str:
    ''' return image sizes attribute from dictonary

    usage: sizes({'60vw':'min-width: 110ch', '95vw': None})
    '''

    sizes_list = (
        f'({sz}) {br}'
        for sz, br
        in criteria.items()
        )
    return ", ".join(sizes_list).replace('(None) ', '')


def _set_img_tag(
        img_tag: bs4.element.Tag,
        image: Image
        ) -> None:

    path = image.path
    url_prefix = current_app.config["IMG_URL"]

    src = _write_src(url_prefix, path, image.thumbnail_widths[0])

    img_tag.attrs.update({  # type: ignore[attr-defined]
        'src': src,
        'srcset': _write_srcset(
            url_prefix,
            path,
            image.thumbnail_widths,
            ),
        'height': image.height,
        'width': image.width,
    })


def _wrap_picture(
        soup: bs4.BeautifulSoup,
        img_tag: bs4.element.Tag,
        image: Image
        ) -> bs4.element.Tag:

    url_prefix = current_app.config["IMG_URL"]
    picture_tag = soup.new_tag('picture')
    source_tag = soup.new_tag('source')
    picture_tag['class'] = img_tag.get('class') or ""
    img_tag['class'] = []
    img_tag.wrap(picture_tag)
    img_tag.insert_before(source_tag)

    source_tag.attrs.update({  # type: ignore[attr-defined]
        'type': 'image/webp',
        'srcset': _write_srcset(
            url_prefix,
            image.path.with_suffix('.webp'),
            image.thumbnail_widths,
            ),
        'sizes': img_tag.get('sizes', '')  # type: ignore[dict-item]
    })
    return picture_tag


def responsive_images(html: str) -> str:
    ''' filter function for jinja templates

    returns html for responsive image syntax
    '''
    soup = bs4.BeautifulSoup(html, 'html.parser')
    img_tags = soup.select('img[data-responsive]')

    for img_tag in img_tags:

        # Check prequistes met:
        # 1) img has a src attribute
        src = img_tag.get('src')
        # 2) img is logged as processed in database
        image = Image.objects.get(name=src)

        if not src or image.status != image.status.PROCESSED:
            continue

        _set_img_tag(img_tag, image)

        if 'no-wrap' not in img_tag['data-responsive']:
            _wrap_picture(soup, img_tag, image)

    return soup.prettify()


def _create_thumbnails(image: Image) -> dict[str, Any]:
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
            _write_src(str(out), image.path, w),
            quality=55, optimize=True, progressive=True
            )
        thumb.save(
            _write_src(str(out), image.path.with_suffix('.webp'), w),
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


def test_compression(image: Image):
    """ Interactive test of image compression quality settings

    Prepares set of thumbnails in tmp/ to allow manual selection of best
    image quality"""

    # Prepare tmp directory
    tmp = Path(IMAGES_ROOT, 'tmp')
    Path.mkdir(tmp)

    # Rotate portrait jpg into correct orientation
    preview = PIL.ImageOps.exif_transpose(PIL.Image.open(image.filepath))

    # Save preview at set quality values
    for qual in [85, 75, 65, 55, 45, 35]:
        preview.thumbnail((1200, 1200))
        # Update save to use relative path
        preview.save(
            f'{tmp}/jpg-{qual}.jpg',
            quality=qual, optimize=True, progressive=True
            )
        preview.save(
            f'{tmp}/webp-{qual}.webp',
            quality=qual, method=6
            )

    # Manually check quality in tmp dir and choose
    qual_jpg = int(input('Chose jpg compression: '))
    set_img_compression(image, '.jpg', qual_jpg)
    qual_webp = int(input('Chose webp compression: '))
    set_img_compression(image, '.webp', qual_webp)

    for _ in Path.iterdir(tmp):
        Path.unlink(_)
    tmp.rmdir()

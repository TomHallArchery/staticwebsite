from pathlib import Path

import PIL
import bs4
from flask import current_app as app

from .models import Img, ImgStatus

# Constants
WIDTHS = app.config["IMG_WIDTHS"]
IMAGES_ROOT = app.config["IMG_ROOT"]
SOURCE_DIR = app.config["IMG_SOURCE_DIR"]
OUTPUT_DIR = app.config["IMG_OUTPUT_DIR"]
IMG_FORMATS = app.config["IMG_FORMATS"]
DEFAULT_IMG_WIDTH = app.config["IMG_DEFAULT_WIDTH"]
IMG_DOMAIN = app.config["IMG_URL"]


def add_all_imgs_to_db():
    '''
    Creates Img model from all image files in source directory

    Used to instantiate database from scratch
    '''
    imgpath = Path(IMAGES_ROOT, SOURCE_DIR)
    for path in Path(imgpath).iterdir():
        Img(name=path.name, type=path.suffix, path=str(path)).save()


def process_img(image: Img):
    ''' save thumbnails and update img database '''
    if image.status == ImgStatus.PROCESSED:
        return
    sizes = _create_thumbnails(image)
    image.update(**sizes)
    image.update(status=ImgStatus.PROCESSED)


def _write_src(img_path: str):
    ''' return image src attribute from prefix url and file name'''
    return Path(IMG_DOMAIN, img_path)


def _write_srcset(path: Path, widths):
    ''' return image srcset attribute for set img widths'''
    srcset_list = (
        f'{_write_src(path.stem)}_{width}{path.suffix} {width}w'
        for width in widths
        )
    return ", ".join(srcset_list)


def _set_img_tag(img: bs4.element.Tag, model: Img):
    path = model._path  # pylint: disable=protected-access

    largest_src = _write_src(
        f"{path.stem}_{str(model.thumbnail_widths[0])}"
        f"{path.suffix}"
        )

    img.attrs.update({
        'src': largest_src,
        'srcset': _write_srcset(
            path,
            model.thumbnail_widths,
            ),
        'height': model.height,
        'width': model.width,
    })


def _wrap_picture(soup: bs4.BeautifulSoup, img: bs4.element.Tag, model: Img):
    picture = soup.new_tag('picture')
    source = soup.new_tag('source')
    picture['class'] = img.get('class')
    img['class'] = []
    img.wrap(picture)
    img.insert_before(source)

    source.attrs.update({
        'type': 'image/webp',
        'srcset': _write_srcset(
            model._path,  # pylint: disable=protected-access
            model.thumbnail_widths,
            ),
        'sizes': img.get('sizes')
    })
    return picture


def responsive_images(html: str):
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
        model = Img.objects.get(name=src)  # pylint: disable=no-member

        if not src or model.status != ImgStatus.PROCESSED:
            continue

        _set_img_tag(img, model)

        if 'no-wrap' not in img.get('data-responsive'):
            _wrap_picture(soup, img, model)

    return soup.prettify()


app.add_template_filter(responsive_images)


def _create_thumbnails(image: Img, widths=WIDTHS):
    """ Generate and save thumbnails of given source image"""
    # open image in PIL
    pil = PIL.ImageOps.exif_transpose(PIL.Image.open(image.path))
    out = Path(IMAGES_ROOT, OUTPUT_DIR)

    widths = list(_select_thumbnail_widths(pil.width, pil.height, widths))
    for w in widths:
        thumb = pil.copy()
        thumb.thumbnail((w, pil.height), resample=PIL.Image.LANCZOS)
        thumb.save(
            f'{out}/{image.name}_{w}.jpg',
            quality=55, optimize=True, progressive=True
            )
        thumb.save(
            f'{out}/{image.name}_{w}.webp',
            quality=55, method=6
            )
    return dict(
        height=pil.width,
        width=pil.height,
        thumbnail_widths=widths,
    )


def _select_thumbnail_widths(width, height, standard_widths):
    '''
    returns list of widths of output images
    '''
    # filter standard widths down
    # to just those smaller than original image dimensions
    sizes = filter(lambda x: max(width, height) > x, standard_widths)

    # correct width descriptor for portrait images
    widths = map(lambda w: min(w, w * width // height), sizes)

    return widths

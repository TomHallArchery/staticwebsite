from pathlib import Path
from collections import Iterable, Collection

import PIL.Image
from PIL.Image import Image as PIL_Image
from PIL.ImageOps import exif_transpose
import bs4
from flask import current_app
from mongoengine.errors import NotUniqueError, DoesNotExist

from .models import Image
from config import Config

# Constants
# Only appear in base config
IMAGES_ROOT = Config.IMG_ROOT
SOURCE_DIR = Config.IMG_SOURCE_DIR
OUTPUT_DIR = Config.IMG_OUTPUT_DIR


# ########################
# Image in HTML functions
# ########################


def _write_src(url_prefix: str, path: Path,
               descriptor: str = None, width: int = None) -> str:
    ''' return image src attribute from prefix url and file name'''
    if width is not None:
        descriptor = f"_{width}"
    url = Path(url_prefix) / path.with_stem(f"{path.stem}{descriptor}").name
    return str(url)


def _write_srcset(url_prefix: str, path: Path, widths: Iterable[int]) -> str:
    ''' return image srcset attribute for set img widths'''

    srcset = (
        f'{_write_src(url_prefix, path, width=width)} {width}w'
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

    src = _write_src(url_prefix, path, width=image.thumbnail_widths[0])

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
        ):

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


# ###############################
# Image database and io functions
#################################


def init_db_from_files() -> None:
    '''
    Creates Image model from all image files in source directory

    Used to instantiate database from scratch
    '''
    img_path = Path(IMAGES_ROOT, SOURCE_DIR)

    for path in img_path.iterdir():
        add_img_to_db(path)


def add_img_to_db(path) -> Image:
    image = Image(
        name=path.name,
        source_format=path.suffix,
        filepath=str(path)
        )
    try:
        image.save()
        print(f"[Saved] Image: {image.name} to db")
    except NotUniqueError:
        print(f"[Skipped] Image: {image.name} already in db")
        pass
    else:
        # record all parameters but don't process images yet
        set_thumbnail_widths(image)
        set_img_format(
            image, '.jpg', quality=55,
            optimize=True, progressive=True
            )
        set_img_format(image, '.webp', quality=55, method=6)
    return image


def delete_images(images: Collection[Image]) -> None:
    for image in images:
        image.path.unlink()
        image.delete()
    print(len(images))


def drop_collection() -> None:
    Image.drop_collection()


def process_img(image: Image, no_write=False) -> None:
    ''' save thumbnails and update img database '''

    create_thumbnails(image)
    image.update(status=image.status.PROCESSED)


def pil_open_img(image: Image) -> PIL_Image:
    ''' Opens image model in PIL '''

    pil: PIL_Image = exif_transpose(PIL.Image.open(image.filepath))
    return pil


def set_img_format(image: Image, format: str, quality: int, **params) -> None:
    try:
        format_info = image.formats.get(format=format)
    except DoesNotExist:
        format_info = Image.Format(
            format=format,
            quality=quality,
            processing=params
            )
        image.formats.append(format_info)
    else:
        format_info.quality = quality
        format_info.processing = params
    finally:
        image.save()


def set_thumbnail_widths(image: Image) -> tuple[int, int, list[int]]:
    """ Generate thumbnail sizes of given source image"""

    # extract original dimensions from oriented image
    with pil_open_img(image) as pil:
        og_width, og_height = pil.width, pil.height

    # filter standard widths down
    # to just those smaller than original image dimensions
    sizes = (x for x in Config.IMG_WIDTHS if max(og_width, og_height) > x)

    # scale width descriptor for portrait images
    widths = (min(s, s * og_width // og_height) for s in sizes)

    image.update(
        width=og_width,
        height=og_height,
        thumbnail_widths=list(widths),
    )
    return og_width, og_height, list(widths)


def create_thumbnails(image: Image) -> None:
    """ save image into thumbnails of given widths """

    pil = pil_open_img(image)
    out = Path(IMAGES_ROOT, OUTPUT_DIR)

    for width in image.thumbnail_widths:
        thumb = pil.copy()
        thumb.thumbnail((width, image.height), resample=PIL.Image.LANCZOS)
        for format in image.formats:
            fname = _write_src(
                str(out),
                image.path.with_suffix(format.format),
                width
                )
            thumb.save(
                fname,
                quality=format.quality,
                **format.processing
                )
            format.outputs.append(fname)
    image.save()
    return


def generate_compressed(image: Image):
    """ Writes image previews to allow comparing compression settings

    Prepares set of thumbnails in tmp/ to allow manual selection of best
    image quality"""

    # Prepare tmp directory
    tmp = Path(IMAGES_ROOT, 'tmp')
    Path.mkdir(tmp, exist_ok=True)

    # Rotate portrait jpg into correct orientation
    pil = pil_open_img(image)

    # Save preview at set quality values
    for qual in [85, 75, 65, 55, 45, 35]:
        preview = pil.copy()
        preview.thumbnail((1200, 1200))
        # Update save to use relative path
        for format in image.formats:
            preview.save(
                f'{tmp}/{format.format[1:]}{qual}{format.format}',
                quality=qual,
                # **format.processing
                )

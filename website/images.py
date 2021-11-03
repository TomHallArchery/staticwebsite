from pathlib import Path
from PIL import Image, ImageOps
from tinydb import Query

from website import app, db, utils

# Constants
WIDTHS = app.config["IMG_WIDTHS"]
IMAGES_ROOT = app.config["IMG_ROOT"]
SOURCE_DIR = app.config["IMG_SOURCE_DIR"]
OUTPUT_DIR = app.config["IMG_OUTPUT_DIR"]
IMG_FORMATS = app.config["IMG_FORMATS"]
IMG_DB = db.table('img')
IQ = Query()
DEFAULT_IMG_WIDTH = app.config["IMG_DEFAULT_WIDTH"]


# Clear img directory
utils.rm_file(Path(IMAGES_ROOT, SOURCE_DIR, '.DS_Store'))


class SiteImage:
    """In Memory representation of the metadata for a saved image asset

    Provides a single handle for all database operations and image processing.
    Also provides html attributes for output """

    def __init__(self, file):
        self.file = file #can't change filename after initialisation
        self.formats = IMG_FORMATS # for now, fixed, as eg saving files depends on assumed formats
        self.db = IMG_DB
        self._dbq = IQ.file == self.file

        assert self.path.suffix in self.formats
        self.format = self.path.suffix

    def __repr__(self):
        return f"SiteImage({self.file})"

    def __eq__(self, other):
        return self.file == other.file

    @property
    def path(self):
        """Returns current relative path to src img file"""
        # Assumes image is inside default image source directory
        abspath = Path(IMAGES_ROOT, SOURCE_DIR, self.file).resolve()
        return abspath.relative_to(Path.cwd())

    @property
    def data(self):
        """ Returns img data from database as dict """
        return self.db.get(self._dbq)

    @property
    def status(self):
        if self.db.contains(self._dbq):
            return self.db.get(self._dbq)["status"]
        return "missing"

    def open(self):
        """ Exposes PIL.Image object, requires closing"""
        self.image = Image.open(self.path)
        return self.image

    def close(self):
        """ Closes PIL.Image object """
        self.image.close()
        self.image = None

    def add_to_db(self):
        """ Inserts new document into image database to represent this image"""
        if not self.data:
            if self.path.exists():
                self.db.insert({"file": self.file, "status": "new"})

    def remove_from_db(self):
        """ Removes document from image database"""
        self.db.remove(self._dbq)

    def update_db(self, values_dict):
        """ Updates document in database with key:value pairs"""
        self.db.update(values_dict, self._dbq)

    def archive(self):
        self.update_db({"status": "archived"})

    def set_compression(self, q, format=".jpg"):
        """ Override default image compression quality """
        # check format is in this instances supported formats
        assert format in self.formats

        self.update_db({
            format : q
            })

    def test_compression(self):
        """ Interactive test of image compression quality settings

        Prepares set of thumbnails in tmp/ to allow manual selection of best
        image quality"""

        #Prepare tmp directory
        tmp = Path(IMAGES_ROOT, 'tmp')
        Path.mkdir(tmp)

        #Rotate portrait jpg into correct orientation
        preview = ImageOps.exif_transpose(self.open())

        #Save preview at set quality values
        for q in [85,75,65,55,45,35]:
            preview.thumbnail((1200,1200))
            # Update save to use relative path
            preview.save(f'{tmp}/jpg-{q}.jpg', quality=q, optimize=True, progressive=True)
            preview.save(f'{tmp}/webp-{q}.webp', quality=q, method=6)

        #Manually check quality in tmp dir and choose
        q1 = int(input(f'Chose jpg compression: '))
        self.set_compression(q1, '.jpg')
        q2 = int(input(f'Chose webp compression: '))
        self.set_compression(q2, '.webp')

        for _ in Path.iterdir(tmp):
            Path.unlink(_)
        tmp.rmdir()

    def create_thumbnails(self, process_src=False):
        """ Generate and save thumbnails of source image"""
        im = ImageOps.exif_transpose(self.open())

        #Deal with fresh images not yet saved in db
        if not self.data:
            self.add_to_db()

        if not process_src:
            if self.data['status'] == "src":
                return
        #Don't process archived images
        if self.data['status'] == "archived":
            return

        q_jpg = self.data.get('.jpg', 55)
        q_webp = self.data.get('.webp', 55)
        width = self.data.get('width')
        height = self.data.get('height')

        #Set up staging area
        out = Path(IMAGES_ROOT, OUTPUT_DIR)
        Path.mkdir(out, exist_ok=True)

        #Produce thumbnails no larger than current image max size
        thumbs = []
        widths = filter(lambda x: max(im.size) > x, WIDTHS)
        for w in widths:
            # Correct width descriptor for portrait images
            _w = min(w, w * width // height)
            thumb = im.copy()
            thumb.thumbnail((w, w), resample=Image.LANCZOS)
            thumb.save(f'{out}/{self.path.stem}_{_w}.jpg', quality=q_jpg, optimize=True, progressive=True)
            thumb.save(f'{out}/{self.path.stem}_{_w}.webp', quality=q_webp, method=6)
            thumbs.append(_w)
        print(thumbs)
        #Save updated data to db
        self.update_db({
            "status": "src",
            "width": im.width,
            "height": im.height,
            "sizes": thumbs
        })
        print("Processed: ", self.path)
        self.close()


class SourceImages:
    """Convinience class for accessing all source images"""
    def __init__(self):
        self.db = IMG_DB
        self.update_archived()

    @property
    def path(self):
        """Returns current relative path to src img directory"""
        # Assumes image is inside default image source directory
        abspath = Path(IMAGES_ROOT, SOURCE_DIR).resolve()
        return abspath.relative_to(Path.cwd())

    @property
    def outpath(self):
        """Returns current relative path to output directory"""
        # Assumes image is inside default image source directory
        abspath = Path(IMAGES_ROOT, OUTPUT_DIR).resolve()
        return abspath.relative_to(Path.cwd())

    @property
    def images(self):
        """ Return list of SiteImage objects from all images in source directory"""
        return [SiteImage(f.name) for f in self.path.iterdir()]

    def find(self, img):
        """ Find one image by filename from images list """
        # i = SiteImage(img)
        if (i := SiteImage(img)) in self.images:
            print("FOUND")
            return i
        print("NOT FOUND")
        return None

    def add_to_db(self):
        for img in self.images:
            img.add_to_db()

    def clear_db(self):
        for img in self.images:
            img.remove_from_db()

    def update_db(self, values_dict):
        """ Updates field in all entries"""
        self.db.update(values_dict)

    def list_db_files(self):
        return [SiteImage(rec['file']) for rec in self.db.all()]

    def update_archived(self):
        """ Tag all images that are in db but not in source as archived """
        for rec in self.list_db_files():
            if rec not in self.images:
                rec.archive()

    def process(self, reprocess=True):
        if reprocess:
            db_imgs = self.db.search(IQ.status.one_of(["new", "src"]))
            for img in db_imgs:
                SiteImage(img['file']).create_thumbnails(process_src=True)
        else:
            db_imgs = self.db.search(IQ.status == "new")
            for img in db_imgs:
                SiteImage(img['file']).create_thumbnails()


def responsive_images(html, conditions, wrap_picture=False):
    img_url = app.config['IMG_URL']
    parser = utils.parse_html(html)
    imgs = parser.getElementsByTagName('img')
    for img in imgs:
        # Abort if img src is empty
        if not img.src:
            continue

        path = Path(img.src)
        si = SiteImage(path.name)

        # Don't process if image not in database; leaves broken img link
        if not si.data:
            continue

        # Set image attributes using database
        sizes = si.data.get('sizes', WIDTHS)
        img.setAttributes({
            'src': Path(img_url, f'{path.stem}_{DEFAULT_IMG_WIDTH}{path.suffix}'),
            'srcset': utils.srcset(img_url, path.stem, sizes, 'jpg'),
            'sizes': utils.sizes(conditions),
            'width': si.data.get('width'),
            'height': si.data.get('height'),
        })

        # Wrap img in picture tag with source for secondary format
        if not wrap_picture:
            continue
        picture = parser.createElement('picture')
        source = parser.createElementFromHTML('<source />')
        parent = img.parentElement

        # wrap img & source with picture
        parent.removeChild(img)
        picture = parent.appendChild(picture)
        picture.appendBlocks([source, img])

        #transfer classes to picture
        for _ in img.getAttribute('class').split():
            cls = img.removeClass(_)
            picture.addClass(cls)

        source.setAttributes({
            'type': 'image/webp',
            'srcset': utils.srcset(img_url, path.stem, sizes, 'webp'),
            'sizes': utils.sizes(conditions)
        })

    return parser.getFormattedHTML()

def main():
    pass

if __name__ == '__main__':
    main()

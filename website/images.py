import os
import subprocess
import hashlib
from PIL import Image, ImageOps
from tinydb import Query

from website import app, db, utils

SIZES = [2000, 1600, 1200, 800, 400]
IMAGES_ROOT = 'website/static/img/'
SOURCE_DIR = 'src'

imgdb = db.table("img")
Img = Query()
utils.rm_file(os.path.join(IMAGES_ROOT, SOURCE_DIR, '.DS_Store'))


vprint = lambda *a: None

class MyImages:
    query = Query()

    def __init__(self, db, root=IMAGES_ROOT):
        self.db = db.table('img')
        self.root = root

def list_images(subdir):
    img_list = [os.path.join(root, file)
                for root, dir, files in os.walk(subdir)
                for file in files
                ]
    return img_list

def get_db_imgs():
    return [rec["file"] for rec in
        imgdb.search(Img.file.exists())]

def check_img_dir(dir):
    img_file_list = os.listdir(dir)
    img_db_list = get_db_imgs()
    delta = list(set(img_file_list) - set(img_db_list))
    delta2 = list(set(img_db_list) - set(img_file_list))
    return delta, delta2

def insert_new_img(img):
    imgdb.insert({"file": img, "status": "new"})

def flag_new_imgs(imgs):
    for img in imgs:
        insert_new_img(img)

def process_new_img(img):
    width, height, q1, q2, thumbs = create_thumbnails(os.path.join(SOURCE_DIR, img), SIZES)
    imgdb.update({
        "status":"src",
        "width": width,
        "height": height,
        "jpg_compression": q1,
        "webp_compression": q2,
        "thumbnail_sizes": thumbs},
         Img.file == img)

def proccess_new_imgs():
    new_imgs = [rec['file'] for rec in
        imgdb.search(Img.status == "new")]
    for img in new_imgs:
        process_new_img(img)

def reset_db():
    imgdb.update({"status": "new"})

def test_compression(imfile):
    path, fname, ext = utils.split_filename(imfile)

    with Image.open(imfile) as im:
        preview = ImageOps.exif_transpose(im)
        # Work in tmp directory: if already in img root this will exist
        os.makedirs('tmp', exist_ok=True)
        for q in [85,75,65,55,45,35]:
            preview.thumbnail((1200,1200))
            preview.save(f'tmp/jpg-{q}.jpg', quality=q, optimize=True, progressive=True)
            preview.save(f'tmp/webp-{q}.webp', quality=q, method=6)


    q1 = input('Chosen jpg compression: ')
    q2 = input('Chosen webp compression: ')
    [ os.remove(_) for _ in list_images('tmp') ]
    return q1, q2

def create_thumbnails(imfile, sizes, q1=55, q2=55):
    ''' Create rezised images from img/new and move original to img/src '''
    path, fname, ext = utils.split_filename(imfile)

    with Image.open(imfile) as im:
        vprint("Loaded image: ", im.filename)
        thumb = ImageOps.exif_transpose(im)
        thumbs = []
        for size in sizes:
            imsize = max(im.size)
            if imsize < size:
                continue
            vprint("Making size: ", size)
            thumb.thumbnail((size, size), resample=Image.LANCZOS)
            thumb.save(f'out/{fname}_{size}.jpg', quality=q1, optimize=True, progressive=True)
            thumb.save(f'out/{fname}_{size}.webp', quality=q2, method=6)
            vprint("Done")
            thumbs.append(size)
    return im.width, im.height, q1, q2, thumbs

def upload_images(dir):
    cmnd = ['python', '-m', 'pynetlify', 'deploy_folder',
     '--site-id', 'bd867c99-8ad2-41da-b295-d619581e8079', dir]
    res = subprocess.run(cmnd)
    print(res)
    # vprint("Uploaded files:")
    # for file in sorted(os.listdir(dir)):
    #     vprint(file)

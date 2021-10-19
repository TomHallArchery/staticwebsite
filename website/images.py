import os
import subprocess
import hashlib
from PIL import Image, ImageOps

from website import app, db, qr, utils

SIZES = [2000, 1600, 1200, 800, 400]
IMAGES_ROOT = 'website/static/img/'

imgdb = db.table("img")

vprint = lambda *a: None

def read_img_dir():
    img_dir_dict = {
        "new" : list_images('new'),
        "src" : list_images('src'),
        "out" : list_images('out')
    }
    return img_dir_dict

def list_images(subdir):
    img_list = [os.path.join(root, file)
                for root, dir, files in os.walk(subdir)
                for file in files
                ]
    return img_list


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


    qj = input('Chosen jpg compression: ')
    qp = input('Chosen webp compression: ')
    [ os.remove(_) for _ in list_images('tmp') ]
    return qj, qp

def create_thumbnails(imfile, sizes, q=55):
    ''' Create rezised images from img/new and move original to img/src '''
    path, fname, ext = utils.split_filename(imfile)

    with Image.open(imfile) as im:
        vprint("Loaded image: ", im.filename)
        thumb = ImageOps.exif_transpose(im)
        for size in sizes:
            imsize = max(im.size)
            if imsize < size:
                continue
            vprint("Making size: ", size)
            thumb.thumbnail((size, size), resample=Image.LANCZOS)
            thumb.save(f'out/{fname}_{size}.jpg', quality=q, optimize=True, progressive=True)
            thumb.save(f'out/{fname}_{size}.webp', quality=q, method=6)
            vprint("Done")

        # size descriptor prefeixed by __s to uniquely identify
        outfile = os.path.join('src', f'{fname}__s{im.width}x{im.height}{ext}')
        vprint(f"Moving image: {outfile}")
        os.rename(imfile, outfile)

def hash_dir_filenames(dir, hashfile):
    ''' Calculates hash of sorted list of files in directory and writes it to hashfile, return True for change in hash '''

    try:
        owd = os.getcwd()
        os.chdir(dir)
        dirlist = ",".join(sorted(os.listdir()))
        new_hash = hashlib.sha256(dirlist.encode()).hexdigest()

        with open(hashfile, "r") as f:
            old_hash = f.read()

        with open(hashfile, "w") as f:
            f.write(new_hash)

    finally:
        os.chdir(owd)

    return new_hash != old_hash
    # eg hash_dir_filenames('website/static/img/out', 'hash.txt')

def upload_images(dir):
    cmnd = ['python', '-m', 'pynetlify', 'deploy_folder',
     '--site-id', 'bd867c99-8ad2-41da-b295-d619581e8079', dir]
    res = subprocess.run(cmnd)
    print(res)
    # vprint("Uploaded files:")
    # for file in sorted(os.listdir(dir)):
    #     vprint(file)

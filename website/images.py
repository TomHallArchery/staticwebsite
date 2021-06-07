from website import app
import os
import sys
import http.server as svr
import subprocess
import argparse
import hashlib
from PIL import Image

SIZES = [2000, 1800, 1600, 1400, 1200, 800, 400]
IMGAES_ROOT = 'website/static/img/'

def read_img_dir():
    img_dir_dict = {
        "new" : os.listdir('new'),
        "src" : os.listdir('src'),
        "out" : os.listdir('out')
    }
    return img_dir_dict

def list_images(subdir):
    return [os.path.join(root, file)
        for root, dir, files in os.walk(subdir)
        for file in files
        ]

def create_thumbnails(imfile, sizes):
    ''' Create rezised images from img/new and move original to img/src '''
    path, file = os.path.split(imfile)
    fname, ext = os.path.splitext(file)

    with Image.open(imfile) as im:
        print("Loaded image: ", im.filename)
        thumb = im.copy()
        for size in sizes:
            if im.width < size:
                continue
            print("Making size: ", size)
            thumb.thumbnail((size, size))
            thumb.save(f'out/{fname}_{size}.jpg', optimize=True, progressive=True)
            thumb.save(f'out/{fname}_{size}.webp', method=6)
            print("Done")

        im.save(f'out/{fname}_{im.width}.jpg', optimize=True, progressive=True)
        im.save(f'out/{fname}_{im.width}.webp', method=6)

        # size descriptor prefeixed by __s to uniquely identify
        outfile = os.path.join('src', f'{fname}__s{im.width}x{im.height}{ext}')
        print(f"Moving image: {outfile}")
        os.rename(imfile, outfile)

def hash_dir_filenames(dir, hashfile):
    ''' Calculates hash of sorted list of files in directory and writes it to hashfile, return True for change in hash '''
    # Deploy static images output to seperate netlify repo
    # Automated deploy if any filenames change (not file contents!)
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
    cmnd = ['python', '-m', 'pynetlify', 'deploy_folder', '--site-id', 'bd867c99-8ad2-41da-b295-d619581e8079', dir]
    res = subprocess.run(cmnd)
    print(res)
    print("Uploaded files:")
    for file in sorted(os.listdir(dir)):
        print(file)



def main(full_reset=False):
    ''' Process all images in img/new '''
    os.chdir(IMGAES_ROOT)
    if os.path.exists('new/.DS_Store'):
        os.remove('new/.DS_Store')
    if os.path.exists('src/.DS_Store'):
        os.remove('src/.DS_Store')

    if full_reset:
        for file in os.listdir('src'):
            print("Input: ", file)
            fname, ext = os.path.splitext(file)
            os.rename(
                os.path.join('src', file),
                # strip size descriptor if present from path/fname__s1234x1234.ext
                os.path.join('new', fname.split('__s')[0] + ext)
                )
        print("files reset from src to new")

    print(list_images('new'))
    for img in list_images('new'):
        create_thumbnails(img, SIZES)

    print(list_images('src'))
    if os.path.exists('out/.DS_Store'):
        os.remove('out/.DS_Store')

    print('Output:')
    print(list_images('out'))



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-S', '--serve', action='store_true')
    parser.add_argument('-R', '--reset', action='store_true')

    args = parser.parse_args()

    main(full_reset=args.reset)

    if args.serve:
        os.chdir('out')
        svr.test(HandlerClass=svr.SimpleHTTPRequestHandler, port=5002)

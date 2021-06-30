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
        "new" : list_images('new'),
        "src" : list_images('src'),
        "out" : list_images('out')
    }
    return img_dir_dict

def rm_file(file):
    if os.path.exists(file):
        os.remove(file)

def list_images(subdir):
    img_list = [os.path.join(root, file)
                for root, dir, files in os.walk(subdir)
                for file in files
                ]
    vprint(img_list)
    return img_list

def fsplit(filepath):
    path, file = os.path.split(filepath)
    fname, ext = os.path.splitext(file)
    return path, file, fname, ext

def test_compression(imfile):
    path, file, fname, ext = fsplit(imfile)

    with Image.open(imfile) as im:
        previw = im.thumbnail(1200,1200)
        for q in [85,75,65,55]:
            preview.save(f'tmp/{fname}_{q}.jpg', quality=q)

def create_thumbnails(imfile, sizes):
    ''' Create rezised images from img/new and move original to img/src '''
    path, file, fname, ext = fsplit(imfile)

    with Image.open(imfile) as im:
        vprint("Loaded image: ", im.filename)
        thumb = im.copy()
        for size in sizes:
            if im.width < size:
                continue
            vprint("Making size: ", size)
            thumb.thumbnail((size, size))
            thumb.save(f'out/{fname}_{size}.jpg', optimize=True, progressive=True)
            thumb.save(f'out/{fname}_{size}.webp', method=6)
            vprint("Done")

        im.save(f'out/{fname}_{im.width}.jpg', optimize=True, progressive=True)
        im.save(f'out/{fname}_{im.width}.webp', method=6)

        # size descriptor prefeixed by __s to uniquely identify
        outfile = os.path.join('src', f'{fname}__s{im.width}x{im.height}{ext}')
        vprint(f"Moving image: {outfile}")
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
    vprint("Uploaded files:")
    for file in sorted(os.listdir(dir)):
        vprint(file)

#TODO: Split main and ifmain into seperate script to avoid runtime warning

def main(reset=False, compress=False):
    ''' Process all images in img/new '''
    os.chdir(IMGAES_ROOT)
    rm_file('new/.DS_Store')
    rm_file('src/.DS_Store')
    imgs = read_img_dir()

    if reset:
        #move all image files back into new/ to reprocess
        #todo: make this work in non flat-directory
        for file in os.listdir('src'): #imgs['src']
            vprint("Input: ", file)
            fname, ext = os.path.splitext(file)
            os.rename(
                os.path.join('src', file),
                # strip size descriptor if present from path/fname__s1234x1234.ext
                os.path.join('new', fname.split('__s')[0] + ext)
                )
        vprint("files reset from src to new")

    if compress:
        print('Interactive Compression')

    vprint(list_images('new'))
    for img in list_images('new'):
        create_thumbnails(img, SIZES)

    vprint(list_images('src'))

    rm_file('out/.DS_Store')
    vprint('Output:')
    vprint(list_images('out'))



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Process website images")
    parser.add_argument('-S', '--serve', action='store_true',
        help="Serve local output directory on port 5002")
    parser.add_argument('-R', '--reset', action='store_true',
        help="Process all existing images as well as new")
    parser.add_argument('-C', '--compress', action='store_true')
    parser.add_argument('-V', '--verbose', action='store_true')
    args = parser.parse_args()

    vprint = print if args.verbose else lambda *a: None

    main(reset=args.reset)

    print(args)
    if args.compress:
        pass

    if args.serve:
        os.chdir('out')
        svr.test(HandlerClass=svr.SimpleHTTPRequestHandler, port=5002)

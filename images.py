import os
import sys
import http.server as svr
import subprocess
import hashlib
from PIL import Image
from website.views import IMAGES_URL

SIZES = [2500, 1500, 1000, 750, 500, 300, 100]
IMGAES_ROOT = 'website/static/img/'

def read_img_dir():
    img_dir_dict = {
        "new" : os.listdir('new'),
        "src" : os.listdir('src'),
        "out" : os.listdir('out')
    }
    return img_dir_dict

def list_new_images():

    return [os.path.join(root, file)
        for root, dir, files in os.walk('new')
        for file in files
        ]

def create_thumbnails(imfile, sizes):
    ''' Create rezised images from img/new and move original to img/src '''
    dir, file = os.path.split(imfile)
    fname, ext = os.path.splitext(file)
    with Image.open(imfile) as im:
        for size in sizes:
            print("Making size: ", size)
            im.thumbnail((size, size))
            im.save(f'out/{fname}_{size}.jpg', optimize=True)
            print("Done")

    os.rename(imfile, os.path.join('src', file))

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


def main():
    ''' Process all images in img/new '''
    print("Images URL: ", IMAGES_URL)
    os.chdir(IMGAES_ROOT)
    for img in list_new_images():
        create_thumbnails(img, SIZES)
    try:
        os.remove('out/.DS_Store')
    except FileNotFoundError:
        pass
    dir = read_img_dir()
    print(dir['out'])


if __name__ == '__main__':
    main()

    print(sys.argv)
    if len(sys.argv) > 1:
        if sys.argv[1] == '-S':
            os.chdir('out')
            svr.test(HandlerClass=svr.SimpleHTTPRequestHandler, port=5002)

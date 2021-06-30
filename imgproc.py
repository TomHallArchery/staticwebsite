from website import app
from website.utils import cwd
from website.images import *

import argparse
import sys
import os
import http.server as svr

def compress(img):
    if not img:
        return
    vprint('Interactive Compression')
    path, file, fname, ext = fsplit(img)
    return test_compression(img)

def main(reset=False):
    ''' Process all images in img/new '''
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

    parser.add_argument('-C', '--compress')
    parser.add_argument('-V', '--verbose', action='store_true')

    args = parser.parse_args()
    vprint = print if args.verbose else lambda *a: None
    print(args)

    compress(args.compress)

    with cwd(IMAGES_ROOT):
        main(reset=args.reset)

    if args.serve:
        os.chdir('out')
        svr.test(HandlerClass=svr.SimpleHTTPRequestHandler, port=5002)

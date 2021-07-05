from website import app, utils
from website.images import *

import argparse
import sys
import os
import http.server as svr

def main():
    ''' Process all images in img/new '''
    parser = argparse.ArgumentParser(description="Process website images")

    parser.add_argument('-S', '--serve', action='store_true',
        help="Serve local output directory on port 5002")

    parser.add_argument('-R', '--reset', action='store_true',
        help="Process all existing images as well as new")

    parser.add_argument('-C', '--compress')
    parser.add_argument('-V', '--verbose', action='store_true')

    args = parser.parse_args()
    vprint = print if args.verbose else lambda *a: None

    #create temp directory with img in various compression qualities
    if args.compress:
        vprint('Interactive Compression')
        imgpath = os.path.abspath(args.compress)
        with cwd(IMAGES_ROOT):
            test_compression(imgpath)

    with cwd(IMAGES_ROOT):
        rm_file('new/.DS_Store')
        rm_file('src/.DS_Store')
        imgs = read_img_dir()

        #move all image files back into new/ to reprocess
        if args.reset:
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

        #create web optimised thumbnails of all new images
        for img in list_images('new'):
            #TODO: add img:quality dict
            create_thumbnails(img, SIZES)

        vprint(list_images('src'))

        rm_file('out/.DS_Store')
        vprint('Output:')
        vprint(list_images('out'))

        if args.serve:
            utils.serve_static('out', 5002)('out')

if __name__ == '__main__':
    main()

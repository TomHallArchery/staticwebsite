import argparse
import sys
import os
import http.server as svr

# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
print(current)

# adding the project directory to
# the sys.path
sys.path.append('/Users/tomhall/dev/projects/tomhallarchery')

from website import app, db, utils, images

def main():
    ''' Process all images in img/new '''
    parser = argparse.ArgumentParser(description="Process website images")

    parser.add_argument('-S', '--serve', action='store_true',
        help="Serve local output directory on port 5002")

    parser.add_argument('-R', '--reset',
        help="Process selected existing images as well as new")

    parser.add_argument('-C', '--compress',
        help="Manually choose compression quality for selected images")

    parser.add_argument('-V', '--verbose', action='store_true')

    args = parser.parse_args()
    vprint = print if args.verbose else lambda *a: None

    # Main Function
    ###

    utils.rm_file('new/.DS_Store')
    utils.rm_file('src/.DS_Store')

    # 1
    # Move selected image files back into new/ to reprocess
    if args.reset:
        #todo: make this work in non flat-directory
        imgpath = args.reset
        vprint("Input: ", imgpath)
        path, fname, ext = utils.split_filename(imgpath)
        os.rename(
            imgpath,
            # strip size descriptor if present from path/fname__s1234x1234.ext
            os.path.join('new', fname.split('__s')[0] + ext)
            )
        vprint("files reset from src to new")

    #2
    # Create temp directory with img in various compression qualities
    if args.compress:
        vprint('Interactive Compression')
        imgpath = os.path.abspath(args.compress)
        images.test_compression(imgpath)

    #3
    # Create web optimised thumbnails of all new images
    for img in images.list_images('new'):
        #TODO: add img:quality dict
        images.create_thumbnails(img, images.SIZES)


    utils.rm_file('out/.DS_Store')
    vprint('Output:')

    if args.serve:
        utils.serve_static('out', 5002)('out')

if __name__ == '__main__':
    main()

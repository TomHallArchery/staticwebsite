from PIL import Image
import argparse
import sys
import io
import os

def main(file):
    os.chdir('website/static/img')
    with Image.open(file) as im:
        print(im.filepath)
        im.save('tmp/test.jpg', quality=5)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=argparse.FileType('rb'), nargs='?', default=sys.stdin)
    args = parser.parse_args()
    print(args)

    main(args.file)

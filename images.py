import os
import sys
import http.server as svr
from PIL import Image
from website.views import IMAGES_URL

SIZES = [2500, 1500, 1000, 750, 500, 300, 100]

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

    # for root, dir, files in os.walk('new'):
    #     for file in files:
    #          print(os.path.join(root, file))



def create_thumbnails(imfile, sizes):
    dir, file = os.path.split(imfile)
    fname, ext = os.path.splitext(file)
    with Image.open(imfile) as im:
        for size in sizes:
            print("Making size: ", size)
            im.thumbnail((size, size))
            im.save(f'out/{fname}_{size}.jpg', optimize=True)
            print("Done")

    os.rename(imfile, os.path.join('src', file))


def main():
    print("Images URL: ", IMAGES_URL)
    os.chdir('website/static/img')
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

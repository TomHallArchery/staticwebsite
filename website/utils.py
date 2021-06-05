import subprocess
import os
import AdvancedHTMLParser
from website import app, flatpages


def compile_css(src, dest, compressed=False, watch=False):
    cmnd = ["sass", f"{src}:{dest}", "--no-source-map"]
    if compressed:
        cmnd.extend([ "-s", "compressed"])
    if watch:
        cmnd.extend(['--watch'])
    res = subprocess.run(cmnd)
    return res

# dirty:
# strip '---' from ._meta attribute of page objects to allow flatpages to work with yaml delimiter
def clean_flatpage_metas(flatpages):
    for page in flatpages:
        page._meta = page._meta.strip('---')

# add filtering method to flatpages object
def filter_pages(path):
    ''' return list of flask flatpage objects from subdirectory of "pages" '''
    return list(page for page in flatpages if os.path.dirname(page.path) == path)



def parse_html(html):
    parser = AdvancedHTMLParser.AdvancedHTMLParser()
    parser.parseStr(html)
    return parser

def split_filename(input):
    path, file = os.path.split(input)
    fname, ext = os.path.splitext(file)
    return (path, fname, ext)

def srcset(img_url, fname, sizes, ext):
    srcset = [f'{img_url + fname}_{size}.{ext} {size}w' for size in sizes]
    return ", ".join(srcset)

def sizes(criteria):
    ''' usage: sizes({'60vw':'min-width: 110ch', '95vw': None}) '''

    sizes = [f'({br}) {sz}' for sz, br in criteria.items()]
    return ", ".join(sizes).replace('(None) ', '')

def main():
    print(sizes({'60vw': 'min-width: 110ch', '95vw': None}))

if __name__ == '__main__':
    main()
# f'({br}) {sz}vw'

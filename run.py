#!/usr/bin/env python
from website import app, flatpages
from website.utils import compile_css
from images import SIZES

app.config['ENV'] = 'DEVELOPMENT'
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

IMAGES_URL = "/static/img/out/"

def pprint(string):
    print(string.center(30, "*"))

# recompile scss on each request during development mode
@app.before_request
def rebuild_css():
    compile_css('website/static/scss', 'website/static/css')


@app.context_processor
def localise_img_url():
    return dict(
        img_url=IMAGES_URL,
        )

if __name__ == '__main__':
    # print config
    pprint("CONFIG")
    for k, v in app.config.items():
        print(f'{k+":":>30} {v}')

    # print pages generated from Markdown
    pprint("PAGES")
    for i,p in enumerate(flatpages):
        print(p.meta.get('title', f'Untitled page at: {p.path}'))

    rebuild_css()

    pprint("LOG")
    app.run(debug=True)

#!/usr/bin/env python

from website import app, flatpages
from website.utils import compile_css

app.config['ENV'] = 'DEVELOPMENT'
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

def pprint(string):
    print(string.center(30, "*"))

# recompile scss on each request during development mode
@app.before_request
def rebuild_css():
    compile_css('website/static/scss', 'website/static/css')

if __name__ == '__main__':
    # print config
    pprint("CONFIG")
    for k, v in app.config.items():
        print(f'{k+":":>30} {v}')

    # print pages generated from Markdown
    pprint("PAGES")
    for p in flatpages:
        print(p.meta['title'])

    rebuild_css()

    pprint("LOG")
    app.run(debug=True)

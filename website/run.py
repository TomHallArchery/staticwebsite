#!/usr/bin/env python

from app import app, flatpages

app.config['ENV'] = 'DEVELOPMENT'
app.config['DEBUG'] = True

def pprint(string):
    print(string.center(30, "*"))

if __name__ == '__main__':
    # print config
    pprint("CONFIG")
    for k, v in app.config.items():
        print(f'{k+":":>30} {v}')

    # print pages generated from Markdown
    pprint("PAGES")
    for p in flatpages:
        print(p.meta['title'])

    pprint("LOG")
    app.run()

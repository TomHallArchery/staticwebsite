#!/usr/bin/env python

from app import app, flatpages

app.config['ENV'] = 'DEVELOPMENT'
app.config['DEBUG'] = True

if __name__ == '__main__':
    # print config
    print("CONFIG".center(30, "*"))
    for k, v in app.config.items():
        print(f'{k+":":>30} {v}')

    # print pages generated from Markdown
    print("PAGES".center(30, "*"))
    for p in flatpages:
        print(p, p.meta)


    app.run()

#!/usr/bin/env python
import subprocess
import os
from time import sleep
from datetime import datetime

from website import app, db, flatpages, utils, database, images

app.config['ENV'] = 'DEVELOPMENT'
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['IMG_URL'] = "/static/img/out/"
REPROC_IMAGES = os.environ.get('REPROC_IMAGES', False)

def pprint(string):
    print(string.center(30, "*"))

# recompile scss on each request during development mode
@app.before_request
def rebuild_css():
    utils.compile_css('website/static/scss', 'website/static/css')

@app.before_first_request
def process_all_images():
    print("Processing images")
    all = images.SourceImages()
    all.add_to_db()
    all.process(reprocess=REPROC_IMAGES)

if __name__ == '__main__':

    # Extra debugging/testing functions
    pprint("LOG")

    # log run
    run = database.Run(started=datetime.now())
    print(run)
    run.save()

    # Run dev server
    app.run(debug=True)

    database.Run.drop_collection()

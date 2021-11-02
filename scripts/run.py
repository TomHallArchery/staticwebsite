#!/usr/bin/env python
from time import sleep
from datetime import datetime

from website import app, flatpages, utils, database, images
import config

app.config.from_object(config.RunConfig)

def pprint(string):
    print(string.center(30, "*"))

@app.before_first_request
def process_all_images():
    print("Processing images")
    all = images.SourceImages()
    all.add_to_db()
    all.process(reprocess= app.config['REPROC_IMAGES'])

if __name__ == '__main__':

    # Extra debugging/testing functions
    pprint("LOG")

    p = utils.compile_css(watch=True)
    print(p.pid)

    # add a comment
    # log run
    database.Run.drop_collection()
    run = database.Run(started=datetime.now())
    print(run)
    run.save()

    # Run dev server
    app.run(debug=True)

#!/usr/bin/env python
import atexit
from datetime import datetime

from website import app, utils, database, images
import config

app.config.from_object(config.RunConfig)


def pprint(string):
    print(string.center(30, "*"))


@app.before_first_request
def process_all_images():
    print("Processing images")
    all_imgs = images.SourceImages()
    all_imgs.add_to_db()
    all_imgs.process(reprocess=app.config['REPROC_IMAGES'])


if __name__ == '__main__':

    # Extra debugging/testing functions
    pprint("LOG")

    sass = utils.compile_css(watch=True)
    atexit.register(sass.kill)

    # log run
    database.Run.drop_collection()
    run = database.Run(started=datetime.now())
    run.save()

    # Run dev server
    app.run(debug=True, port=5000)

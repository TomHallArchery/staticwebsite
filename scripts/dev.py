#!/usr/bin/env python
import atexit
from datetime import datetime
import livereload as lr

from website import create_app, utils, database
import config

app = create_app(config.DevConfig)


if __name__ == '__main__':

    with app.app_context():
        sass = utils.compile_css(watch=True)
        atexit.register(sass.kill)

        # log run
        database.Run.drop_collection()
        run = database.Run(started=datetime.now())
        run.save()

    # Run dev server
    server = lr.Server(app.wsgi_app)
    server.watch('website')
    server.serve(port=5000, liveport=5001)
    # app.run(port=5000)

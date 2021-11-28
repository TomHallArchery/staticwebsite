#!/usr/bin/env python
import atexit
from datetime import datetime
import livereload as lr

from website import create_app, utils, models
import config

app = create_app(config.DevConfig)


if __name__ == '__main__':

    sass = utils.compile_css(app, watch=True)
    atexit.register(sass.kill)

    with app.app_context():
        # log run
        models.Run.drop_collection()
        run = models.Run(started=datetime.now())
        run.save()

    # Run dev server
    server = lr.Server(app.wsgi_app)
    server.watch('website')
    server.serve(port=5001)
    # app.run(port=5000)

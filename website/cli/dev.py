#!/usr/bin/env python
from datetime import datetime
import livereload as lr

from website import create_app, utils, models
import config

app = create_app(config.DevConfig)

def sass():
    return utils.compile_css(app)

if __name__ == '__main__':

    with app.app_context():
        # log run
        models.Run.drop_collection()
        run = models.Run(started=datetime.now())
        run.save()

    sass()

    # Run dev server
    server = lr.Server(app.wsgi_app)
    server.watch('website/static/scss/**/*.scss', func=sass)
    server.watch('website')
    server.serve(port=5001)
    # app.run(port=5000)

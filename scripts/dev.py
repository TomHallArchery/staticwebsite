#!/usr/bin/env python
import atexit
from datetime import datetime

from website import create_app, utils, database
import config

app = create_app()
app.config.from_object(config.DevConfig)


if __name__ == '__main__':

    with app.app_context():
        sass = utils.compile_css(watch=True)
        atexit.register(sass.kill)

        # log run
        database.Run.drop_collection()
        run = database.Run(started=datetime.now())
        run.save()

    # Run dev server
    app.run(debug=True, port=5000)

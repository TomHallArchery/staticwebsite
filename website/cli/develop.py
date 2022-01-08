#!/usr/bin/env python
import livereload as lr

import config
from website import create_app

from . import cli_bp as bp
from .utils import compile_css


@bp.cli.command('develop')
def main():
    """ Run a hot reloading development server on port 5001 """

    app = create_app(config.DevConfig)

    def sass():
        return compile_css(app)

    sass()

    # Run dev server
    server = lr.Server(app.wsgi_app)
    server.watch('website/static/scss/**/*.scss', func=sass)
    server.watch('website')
    server.serve(port=5001)


if __name__ == '__main__':
    main()

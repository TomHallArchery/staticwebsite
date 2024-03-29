#!/usr/bin/env python
from pathlib import Path

import click
import flask

import config
from website import create_app, freezer

from . import cli_bp as bp
from .utils import compile_css


@bp.cli.command('freeze')
@click.option('--serve', is_flag=True)
@click.option('--deployment', is_flag=True)
def main(serve, deployment):
    ''' Freeze website into static files '''

    if deployment:
        app = create_app(config.DeployConfig)
    else:
        app = create_app(config.ProdConfig)

    # Instructs the freezer to also check for dynamically generated urls
    # from serve_page functinon.
    @freezer.register_generator
    def register_fonts():
        ''' Register font files with frozen flask '''
        fonts = app.config["FONTS"]
        for path, font in fonts.items():
            file = Path('fonts', path, font)
            yield flask.url_for('static', filename=str(file))

    click.echo("Building website:")

    # TODO: check font files exist and compile with pyftsubset

    # Freeze static files into default directory 'build'
    assert app.cfg == freezer.app.cfg
    freezer.freeze()
    click.echo("Website frozen")

    compile_css(app, compressed=True)
    click.echo("Css recompiled")

    # Frozen flask issue:
    # have to manually build the 404 error page for use by server
    with app.test_request_context():
        error_page = flask.render_template('generic/404.html.j2')
        with open('website/build/404.html', 'w', encoding="utf-8") as f:
            f.write(error_page)

    if serve:
        freezer.serve()


if __name__ == '__main__':
    main()

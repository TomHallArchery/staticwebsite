# Download build and store latest alpine.js files in static,
# choosing type by config
import os
import requests

from website import create_app
from . import cli_bp as bp
import config


@bp.cli.command('vendorize')
def main():
    app = create_app(config.Config)

    alpine_version = app.config["ALPINE_VERSION"]
    alpine_file_path = app.config["ALPINE_FILE_PATH"]

    alpine_url = f"https://unpkg.com/alpinejs@{alpine_version}/dist/cdn.min.js"
    alpine = requests.get(alpine_url)

    if alpine.ok:
        os.makedirs(os.path.dirname(alpine_file_path), exist_ok=True)
        with open(alpine_file_path, 'w') as f:
            f.write(alpine.text)

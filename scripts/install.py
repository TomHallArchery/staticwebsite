# Download build and store latest alpine.js files in static, choosing type by config
import requests
from pathlib import Path

from website import app, utils

alpine_url= app.config["ALPINE"]['url']
alpine_file_path = app.config["ALPINE"]['fpath']

js = requests.get(alpine_url)
# js = f"console.log({alpine_url})"

if js.ok:
    with open(alpine_file_path, 'w') as f:
        f.write(js.text)

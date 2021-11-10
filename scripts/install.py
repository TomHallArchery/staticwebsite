# Download build and store latest alpine.js files in static,
# choosing type by config
import os
import requests

from website import create_app

app = create_app
app.config.from_object(config.Config)

alpine_url = app.config["ALPINE"]['url']
alpine_file_path = app.config["ALPINE"]['fpath']

js = requests.get(alpine_url)

if js.ok:
    os.makedirs(os.path.dirname(alpine_file_path), exist_ok=True)
    with open(alpine_file_path, 'w') as f:
        f.write(js.text)

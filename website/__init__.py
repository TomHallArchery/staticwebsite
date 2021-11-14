from flask import Flask
from flask_flatpages import FlatPages
from tinydb import TinyDB

import config

app = Flask(__name__)
# reads database in from json file
db = TinyDB('database.json', indent=4, separators=(',', ': '))

app.config.from_object(config.Config)
flatpages = FlatPages(app)

from website import utils, database, images, errors, views

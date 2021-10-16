from tinydb import TinyDB, Query

from website import app

db = TinyDB('database.json')

def clear_db():
    db.truncate()

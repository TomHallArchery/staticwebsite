import mongoengine as mg

from website import app

# connect
mg.connect(
    'website',  # connects to website DB
    username="app",
    password=app.config["DB_PWD"],
    authentication_source="admin",
    port=app.config["DB_PORT"],
    )


# creates or loads collection
class Img(mg.Document):
    name = mg.StringField()
    desc = mg.StringField()
    created_at = mg.DateTimeField()


class Page(mg.Document):
    title = mg.StringField()
    content = mg.StringField()


class Run(mg.Document):
    started = mg.DateTimeField()

import mongoengine as mg

from flask import current_app as app


# connect
def connect_db():
    ''' connect to default mongodb database '''
    mg.connect(
        'website',  # connects to website DB
        username="app",
        password=app.config["DB_PWD"],
        authentication_source="admin",
        port=app.config["DB_PORT"],
        )


# creates or loads collection
class Img(mg.Document):
    ''' Image ODM '''
    name = mg.StringField()
    desc = mg.StringField()
    created_at = mg.DateTimeField()


class Page(mg.Document):
    ''' Page ODM '''
    title = mg.StringField()
    content = mg.StringField()


class Run(mg.Document):
    ''' Run ODM '''
    started = mg.DateTimeField()


if __name__ == '__main__':
    connect_db()

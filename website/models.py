from enum import Enum
from pathlib import Path

import mongoengine as mg

from website import db


# creates or loads collection
class Img(db.Document):
    ''' Image ODM '''

    class Status(Enum):
        ''' Img status enumerator '''
        NEW = 'new'
        PROCESSED = 'processed'
        ARCHIVED = 'archived'

    # Status = Enum('Status', 'NEW PROCESSED ARCHIVED')

    name = mg.StringField(required=True, unique=True)
    type = mg.StringField(required=True)
    path = mg.StringField()
    desc = mg.StringField()
    status = mg.EnumField(Status, default=Status.NEW)
    width = mg.IntField()
    height = mg.IntField()
    thumbnail_widths = mg.ListField(mg.IntField())

    def __repr__(self):
        return f"<Img(name='{self.name})', {self.status}>"

    @property
    def _path(self):
        return Path(self.path)


class Page(db.Document):
    ''' Page ODM '''
    title = mg.StringField()
    content = mg.StringField()


class Run(db.Document):
    ''' Run ODM '''
    started = mg.DateTimeField()


if __name__ == '__main__':
    pass

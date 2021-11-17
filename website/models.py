from enum import Enum

import mongoengine as mg

from website import db


class ImgStatus(Enum):
    NEW = 'new'
    PROCESSED = 'processed'
    ARCHIVED = 'archived'


# creates or loads collection
class Img(db.Document):
    ''' Image ODM '''
    name = mg.StringField(required=True)
    type = mg.StringField(required=True)
    path = mg.StringField()
    desc = mg.StringField()
    status = mg.EnumField(ImgStatus, default=ImgStatus.NEW)
    width = mg.IntField()
    height = mg.IntField()
    thumbnail_widths = mg.ListField(mg.IntField())

    def __repr__(self):
        return f"Img({self.name})"

    @property
    def _path(self):
        from pathlib import Path
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

from enum import Enum
from pathlib import Path

from .. import db


class Img(db.Document):
    ''' Image ODM '''

    class Status(Enum):
        ''' Img status enumerator '''
        NEW = 'new'
        PROCESSED = 'processed'
        ARCHIVED = 'archived'

    # Status = Enum('Status', 'NEW PROCESSED ARCHIVED')

    name = db.StringField(required=True, unique=True)
    type = db.StringField(required=True)
    filepath = db.StringField()
    desc = db.StringField()
    status = db.EnumField(Status, default=Status.NEW)
    width = db.IntField()
    height = db.IntField()
    thumbnail_widths = db.ListField(db.IntField())

    def __repr__(self):
        return f"<Img(name='{self.name}'), {self.status.name}, db.Document>"

    @property
    def path(self) -> Path:
        return Path(self.filepath)

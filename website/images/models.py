from enum import Enum
from pathlib import Path

from website import db


class ImgStatus(Enum):
    ''' Img status enumerator '''

    NEW = 'new'
    PROCESSED = 'processed'
    ARCHIVED = 'archived'


class Img(db.Document):  # type: ignore[name-defined]
    ''' Image ODM '''

    name = db.StringField(required=True, unique=True)
    type = db.StringField(required=True)
    filepath = db.StringField()
    desc = db.StringField()
    status = db.EnumField(ImgStatus, default=ImgStatus.NEW)
    width = db.IntField()
    height = db.IntField()
    thumbnail_widths = db.ListField(db.IntField())

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Img(name='{self.name}'), {self.status.name}>"

    @property
    def path(self) -> Path:
        return Path(self.filepath)

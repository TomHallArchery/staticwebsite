from enum import Enum
from pathlib import Path

from website import db


class ImgStatus(Enum):
    ''' Img status enumerator '''

    NEW = 'new'
    PROCESSED = 'processed'
    ARCHIVED = 'archived'


class ImageFormat(db.EmbeddedDocument):  # type: ignore[name-defined]
    ''' Image format subdocument '''
    FORMATS = ('.jpg', '.webp')
    type = db.StringField(choices=FORMATS, default='.jpg')
    quality = db.IntField(min=0, max=100, default=55)


class Image(db.Document):  # type: ignore[name-defined]
    ''' Image ODM '''

    name = db.StringField(required=True, unique=True)
    type = db.StringField(required=True)
    filepath = db.StringField()
    desc = db.StringField()
    status = db.EnumField(ImgStatus, default=ImgStatus.NEW)
    width = db.IntField()
    height = db.IntField()
    thumbnail_widths = db.ListField(db.IntField())
    formats = db.ListField(db.EmbeddedDocumentField(ImageFormat))

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Img(name='{self.name}'), {self.status.name}>"

    @property
    def path(self) -> Path:
        return Path(self.filepath)

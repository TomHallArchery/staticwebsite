from enum import Enum
from pathlib import Path

from slugify import slugify
import frontmatter as fmr


from website import db


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


class Page(db.Document):
    ''' Page ODM '''

    class Status(Enum):
        ''' Img status enumerator '''
        DRAFT = 'draft'
        PUBLISHED = 'published'
        ARCHIVED = 'archived'

    title = db.StringField(required=True, unique=True)
    description = db.StringField(required=True)
    filepath = db.StringField()
    keywords = db.ListField(db.StringField())
    author = db.StringField(default="Tom Hall")
    status = db.EnumField(Status, default=Status.DRAFT)
    slug = db.StringField()

    @property
    def _slug(self):
        return slugify(self.title)

    @property
    def path(self):
        return Path(self.filepath)

    def parse_file(self):
        post = fmr.load(self.filepath)
        return post


class Run(db.Document):
    ''' Run ODM '''
    started = db.DateTimeField()


if __name__ == '__main__':
    pass

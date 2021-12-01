from enum import Enum
from pathlib import Path

from slugify import slugify
import frontmatter as fmr

from website import db


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

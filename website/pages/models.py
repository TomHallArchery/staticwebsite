from enum import Enum
from pathlib import Path

from slugify import slugify

from website import db


class Page(db.Document):  # type: ignore[name-defined]
    ''' Page ODM '''

    class Status(Enum):
        ''' Page status enumerator '''
        DRAFT = 'draft'
        PUBLISHED = 'published'
        ARCHIVED = 'archived'

    name = db.StringField(required=True, unique=True)
    filepath = db.StringField(unique=True)
    status = db.EnumField(Status, default=Status.DRAFT)

    # Keys from page metadata,
    # read/write to markdown?

    title = db.StringField()
    description = db.StringField()
    keywords = db.ListField(db.StringField())
    author = db.StringField(default="Tom Hall")
    slug = db.StringField()
    header_image = db.StringField()
    layout = db.StringField(default="default")  # ?

    def slugify(self):
        return slugify(self.title)

    @property
    def path(self):
        return Path(self.filepath)

    def __repr__(self):
        return f"<Page(name='{self.name}'), {self.status.name}, db.Document>"


class Pages():
    """ Holds shortcuts for queries on Document collection

    Note: Cannot access collection.objects unless working within app context,
    so only safe to use within definitions. """
    collection = Page
    # could extend this into an abstract Documents class that uses classmethods
    # to create these automatically for multiple collections

    def query(**kwargs):
        return Page.objects(**kwargs)

    def get(**kwargs):
        return Page.objects.get(**kwargs)

    def get_or_404(**kwargs):
        return Page.objects.get_or_404(**kwargs)

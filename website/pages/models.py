from datetime import datetime
from enum import Enum
import json
from pathlib import Path

from slugify import slugify  # type: ignore[import]
import frontmatter

from website import db
from website.images.models import Img


class PageStatus(Enum):
    ''' Page status enumerator '''
    DRAFT = 'draft'
    PUBLISHED = 'published'
    ARCHIVED = 'archived'
    TEST = 'test'


class PageMeta(db.DynamicEmbeddedDocument):  # type: ignore[name-defined]
    ''' Embedded page metadata ODM '''
    title = db.StringField()
    description = db.StringField()
    keywords = db.ListField(db.StringField())
    author = db.StringField(default="Tom Hall")
    slug = db.StringField()
    header_image = db.ReferenceField(Img)
    layout = db.StringField(default="default")
    date_created = db.DateTimeField(default=datetime.utcnow)
    date_published = db.DateTimeField()

    @property
    def all(self):
        return json.loads(self.to_json())

    def __str__(self):
        return f"{list(self.all)}"

    def __repr__(self):
        return f"<PageMeta, {len(self.all)} items>"


class Page(db.Document):  # type: ignore[name-defined]
    ''' Page ODM '''

    name = db.StringField(required=True, unique=True)
    filepath = db.StringField(unique=True)
    status = db.EnumField(PageStatus, default=PageStatus.DRAFT)
    metadata = db.EmbeddedDocumentField(PageMeta, default=PageMeta)
    content = db.StringField()
    # Keys from page metadata,
    # read/write to markdown?
    meta = {
        'indexes': [
            'name',
        ]
    }

    @property
    def slug(self):
        if slug := self.metadata.slug:
            return slugify(slug)
        elif title := self.metadata.title:
            return slugify(title)
        else:
            return slugify(self.name)

    @property
    def path(self):
        return Path(self.filepath)

    def parse_file(self):
        return frontmatter.load(self.filepath)

    def pull_from_file(self):
        file = self.parse_file()
        for k, v in file.metadata.items():
            setattr(self.metadata, k, v)
        self.content = f"{file.content[:120]}..."
        self.save()
        return file.metadata

    def push_to_file(self):
        file = self.parse_file()
        metadata = json.loads(self.metadata.to_json())
        file.metadata = metadata
        frontmatter.dump(file, self.path)
        return metadata

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"<Page(name='{self.name}'), {self.status.name}, db.Document>"


class Pages():
    """ Holds shortcuts for queries on Document collection

    Note: Cannot access collection.objects unless working within app context,
    so only safe to use within definitions.
    """
    collection = Page
    # could extend this into an abstract Documents class that uses classmethods
    # to create these automatically for multiple collections

    @staticmethod
    def query(**query):
        return Page.objects(**query)

    @staticmethod
    def get(**query):
        return Page.objects.get(**query)

    @staticmethod
    def get_or_404(**query):
        return Page.objects.get_or_404(**query)

    @staticmethod
    def name(name):
        return Page.objects.get(name=name)

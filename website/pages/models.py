from datetime import date
from enum import Enum
from pathlib import Path
from typing import Any

import frontmatter
from mongoengine import signals
from mongoengine.queryset import queryset_manager
from slugify import slugify  # type: ignore[import]

from website import db
from website.images.models import Image


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
    header_image = db.ReferenceField(Image)
    layout = db.StringField(default="default")
    date_created = db.DateTimeField(default=date.today)
    date_published = db.DateTimeField()

    @property
    def all(self):
        return self.to_mongo().to_dict()

    def __str__(self):
        return f"{list(self.all)}"

    def __repr__(self):
        return f"<PageMeta, {len(self.all)} items>"


class Page(db.Document):  # type: ignore[name-defined]
    ''' Page ODM '''

    # Document Fields

    name = db.StringField(required=True, unique=True)
    filepath = db.StringField(unique=True)
    status = db.EnumField(PageStatus, default=PageStatus.DRAFT)
    metadata = db.EmbeddedDocumentField(PageMeta, default=PageMeta)
    content = db.StringField()

    meta = {'indexes': ['name']}

    # Derived data
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

    # CRUD
    @classmethod
    def create_by_name(cls, name: str) -> 'Page':
        page = cls(name=name)
        page.filepath = f'website/content/draft/{name}.md'
        page.path.touch()
        page.save()
        return page

    @staticmethod
    def delete_handler(sender, document):
        print("sender", sender)
        print("delete handler running on", document)
        document.path.unlink()

    # Buisness logic
    def publish(self) -> None:
        self.status = PageStatus.PUBLISHED
        self.metadata.date_published = date.today()

    def revert(self) -> None:
        self.status = PageStatus.DRAFT
        del self.metadata.date_published

    # Metadata syncing
    def _parse_file(self):
        return frontmatter.load(self.filepath)

    def file_content(self) -> str:
        return self._parse_file().content

    def file_meta(self) -> dict[str, Any]:
        return self._parse_file().metadata

    def pull_from_file(self):
        file = self._parse_file()
        for k, v in file.metadata.items():
            setattr(self.metadata, k, v)
        self.content = file.content
        self.save()
        return file.metadata

    def push_to_file(self):
        self.path.touch()
        file = self._parse_file()
        metadata = self.metadata.to_mongo().to_dict()
        file.metadata = metadata
        file.content = self.content
        frontmatter.dump(file, self.path)
        return metadata

    # Queryset Managers
    @queryset_manager
    def published(cls, queryset):
        return queryset.filter(status=PageStatus.PUBLISHED)

    # Display
    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return (
            f"<Page(name='{self.name}', "
            f"filepath='{self.filepath}'), "
            f"{self.status.name}>"
            )


signals.post_delete.connect(Page.delete_handler, sender=Page)

from datetime import date
from enum import Enum
from pathlib import Path
from typing import Any

import frontmatter
from flask import Markup, render_template_string
from markdown import markdown  # type: ignore[import]
from mongoengine import signals
# from mongoengine.errors import NotUniqueError
from mongoengine.queryset import queryset_manager
from slugify import slugify  # type: ignore[import]

from config import Config
from website import db
from website.images.models import Image

from . import pages_bp as bp


@bp.app_template_filter()
def prerender_jinja(text: str) -> str:
    ''' render flask templating in markdown pages before parsing markdown '''
    prerendered_body = render_template_string(Markup(text))
    html = markdown(
        prerendered_body,
        extensions=Config.CONTENT_MARKDOWN_EXTENSIONS,
        output_format='html5',  # type: ignore[arg-type]
        # 'html5' not in stubs library
        )
    return html


class PageStatus(Enum):
    ''' Page status enumerator '''
    NULL = None
    DRAFT = 'draft'
    PUBLISHED = 'published'
    ARCHIVED = 'archived'
    TEST = 'test'


class Page(db.Document):  # type: ignore[name-defined]
    ''' Page ODM '''

    # Document Fields
    name = db.StringField(required=True, unique=True)
    filepath = db.StringField(unique=True)
    status = db.EnumField(PageStatus, default=PageStatus.NULL)

    # metadata
    title = db.StringField()
    description = db.StringField()
    keywords = db.ListField(db.StringField())
    author = db.StringField(default="Tom Hall")
    slug = db.StringField()
    link = db.StringField()
    header_image = db.ReferenceField(Image)
    layout = db.StringField(default="default")
    date_created = db.DateTimeField(default=date.today)
    date_published = db.DateTimeField()

    # content: define last to leave out of fields property
    content = db.StringField()

    meta = {'indexes': ['name']}

    # Derived data
    def get_slug(self):
        if slug := self.slug:
            return slugify(slug)
        elif title := self.title:
            return slugify(title)
        else:
            return slugify(self.name)

    @property
    def path(self):
        return Path(self.filepath)

    @property
    def fields(self):
        """List all field names except id, content for export"""
        return [field for field in self][1:-1]

    # CRUD
    @classmethod
    def create_by_name(cls, name: str) -> 'Page':
        page = cls(name=name)
        page.filepath = f'website/content/draft/{name}.md'
        page.path.touch()
        return page

    @staticmethod
    def delete_handler(sender, document):
        print("delete handler running on", document)
        document.path.unlink()

    @staticmethod
    def save_handler(sender, document, created):
        print("save handler running on", document)
        document.push_to_file()

    @staticmethod
    def init_handler(sender, document, values):
        pass
        # print("init handler running on values dict", values['name'])

    # Buisness logic
    def publish(self) -> None:
        self.status = PageStatus.PUBLISHED
        self.date_published = date.today()

    def revert(self) -> None:
        self.status = PageStatus.DRAFT
        del self.date_published

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
            setattr(self, k, v)
        self.content = file.content
        return file.metadata

    def push_to_file(self):
        self.path.touch()
        # serialise mongo fields and clean up
        metadata = {k: self[k] for k in self.fields}
        metadata['status'] = self.status.value
        metadata['keywords'] = list(self.keywords)

        file = self._parse_file()
        file.metadata = metadata
        file.content = self.content
        frontmatter.dump(file, self.path)
        return metadata

    def render_content(self):
        return prerender_jinja(self.file_content())

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
signals.post_save.connect(Page.save_handler, sender=Page)
signals.pre_init.connect(Page.init_handler, sender=Page)


def init_db() -> None:
    '''
    Creates Page model from all markdown files in pages directory

    Used to instantiate database from scratch
    '''
    content_path = Path('website/content')
    for fn in content_path.rglob('*.md'):

        page = Page.objects(name=fn.stem).modify(
            upsert=True,
            new=True,
            set__filepath=str(fn),
            )
        page.pull_from_file()
        page.save()

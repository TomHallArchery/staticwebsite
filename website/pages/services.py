"""
Service functions for CRUD operations on Page objects

file_content: utility function, returns formatted body html
from Page objects referenced file.
file_meta: Utility function, returns metadata dictionary
from Page objects referenced file.
"""
from typing import Any
from pathlib import Path

import frontmatter as fmr
from flask import render_template_string, Markup
from mongoengine.errors import NotUniqueError
from markdown import markdown  # type: ignore[import]

from config import Config
from .models import Page, Pages


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


def render_page_args(**query):
    """ Shortcut function to help render standard page """
    page = Pages.get_or_404(**query)
    sidebar = Pages.get(name='sidebar')

    return dict(
        content=file_content(page),
        side=file_content(sidebar),
        title=page.metadata.title,
        description=page.metadata.description,
        keywords=page.metadata.keywords,
    )


def file_content(page: Page) -> str:
    assert page.path.suffix == '.md'
    return prerender_jinja(fmr.load(page.path).content)


def file_meta(page: Page) -> dict[str, Any]:
    assert page.path.suffix == '.md'
    return fmr.load(page.path).metadata


def select_page_by_name(name: str) -> Page:
    page = Pages.name(name)
    return page


def create_page(name: str) -> Page:
    page = Page(name=name)
    page.filepath = f'website/content/{name}.md'
    page.path.touch()
    page.save()
    return page


def delete_page(name: str) -> None:
    pages = Pages.query(name=name)  # type: ignore[arg-type]
    for page in pages:
        page.path.unlink()
        page.delete()


def init_db_from_files() -> None:
    '''
    Creates Page model from all markdown files in pages directory

    Used to instantiate database from scratch
    '''
    content_path = Path('website/content')
    for fn in content_path.rglob('*.md'):
        page = Page(
            filepath=str(fn),
            name=fn.stem,
            )
        try:
            page.save()
            print(f"[Saved] Page: {page.name} to db")  # convert to log.info
        except NotUniqueError:
            # TODO convert to log.debug
            print(f"[Skipped] Page: {page.name} already in db")
            continue
        else:
            page.pull_from_file()


def drop_collection() -> None:
    Page.drop_collection()

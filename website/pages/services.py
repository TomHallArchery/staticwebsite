from pathlib import Path
from typing import Any

from flask import render_template_string, Markup
import frontmatter as fmr
from mongoengine.errors import NotUniqueError
from markdown import markdown

from config import Config
from .models import Page, Metadata


def add_all_pages_to_db() -> None:
    '''
    Creates Page model from all markdown files in pages directory

    Used to instantiate database from scratch
    '''
    content_path = Path('website/content')
    for fn in content_path.rglob('*.md'):
        raw_metadata = fmr.load(fn).metadata
        metadata = Metadata(**raw_metadata)

        page = Page(
            filepath=str(fn),
            name=fn.stem,
            metadata=metadata
            )
        try:
            page.save()
            print(f"[Saved] Page: {page.name} to db")  # convert to log.info
        except NotUniqueError:
            # convert to log.debug
            print(f"[Skipped] Page: {page.name} already in db")

            continue
        # _read_metadata_from_file(page)


def _read_metadata_from_file(page: Page) -> dict:
    return meta(page)
    # page.modify(
    #     title=m.get('title', ''),
    #     description=m.get('description', ''),
    #     keywords=m.get('keywords', ''),
    #     )


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


def content(page: Page) -> str:
    assert page.path.suffix == '.md'
    return prerender_jinja(fmr.load(page.path).content)


def meta(page: Page) -> dict[str, Any]:
    assert page.path.suffix == '.md'
    return fmr.load(page.path).metadata

from pathlib import Path
from typing import Any

from flask import render_template_string, Markup
import frontmatter as fmr
from mongoengine.errors import NotUniqueError
from markdown import markdown

from config import Config
from .models import Page


def add_all_pages_to_db() -> None:
    '''
    Creates Page model from all markdown files in pages directory

    Used to instantiate database from scratch
    '''
    content_path = Path('website/content')
    for fn in content_path.rglob('*.md'):
        page = Page(
            filepath=str(fn),
            name=fn.stem
            )
        try:
            page.save()
            m = meta(page)
            page.modify(
                title=m.get('title', ''),
                description=m.get('description', ''),
                keywords=m.get('keywords', ''),
                )
            print(f"[Saved] Page: {page.name} to db")
        except NotUniqueError:
            print(f"[Skipped] Page: {page.name} already in db")
            continue


def prerender_jinja(text: str) -> str:
    ''' render flask templating in markdown pages before parsing markdown '''
    prerendered_body = render_template_string(Markup(text))
    # Setting flatpages extensions wasn't working for some reason
    # had to overwrite pygmented_markdown method
    html = markdown(
        prerendered_body,
        extensions=Config.FLATPAGES_MARKDOWN_EXTENSIONS,
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

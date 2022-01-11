"""
"""
from pathlib import Path

from flask import Markup, render_template_string
from markdown import markdown  # type: ignore[import]
from mongoengine.errors import NotUniqueError

from config import Config

from . import pages_bp as bp
from .models import Page


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


def render_page_args(**query):
    """ Shortcut function to help render standard page """
    page = Pages.get_or_404(**query)
    sidebar = Pages.get(name='sidebar')

    return dict(
        content=prerender_jinja(page.content),
        side=prerender_jinja(sidebar.content),
        title=page.metadata.title,
        description=page.metadata.description,
        keywords=page.metadata.keywords,
    )


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
            print(f"[Saved] {page!r}")  # convert to log.info
        except NotUniqueError:
            # TODO convert to log.debug
            print(f"[Skipped] Page: {page.name} already in db")
            continue
        else:
            page.pull_from_file()

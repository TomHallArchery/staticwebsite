from pathlib import Path

from mongoengine.errors import NotUniqueError
import frontmatter as fmr

from website.models import Page


def add_all_pages_to_db() -> None:
    '''
    Creates Page model from all markdown files in pages directory

    Used to instantiate database from scratch
    '''
    for fn in Path('website/pages').rglob('*.md'):
        post = fmr.load(fn)

        page = Page(
            title=post.get('title', fn.name),
            description=post.get('description', ''),
            filepath=str(fn)
            )
        try:
            page.slug = page._slug
            page.save()
            print(f"[Saved] Page: {page.title} to db")
        except NotUniqueError:
            print(f"[Skipped] Page: {page.title} already in db")
            continue


def overwrite_metadata(page: Page):
    page.to_json()

from markdown import markdown
from flask import render_template_string, Markup
import config

def prerender_jinja(text: str) -> str:
    ''' render flask templating in markdown pages before parsing markdown '''
    prerendered_body = render_template_string(Markup(text))
    # Setting flatpages extensions wasn't working for some reason
    # had to overwrite pygmented_markdown method
    html = markdown(
        prerendered_body,
        extensions=config.Config.FLATPAGES_MARKDOWN_EXTENSIONS,
        output_format='html5',  # type: ignore[arg-type]
        # 'html5' not in stubs library
        )
    return html

from flask import current_app as app
app.add_template_filter(prerender_jinja)

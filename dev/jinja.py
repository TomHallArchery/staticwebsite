from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
import sys
import click

@click.command()
@click.argument('tmpl_path')
@click.argument('md_path')
def template_markdown(tmpl_path, md_path):
    env = Environment(
        loader = FileSystemLoader('templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    tmpl = env.get_template(tmpl)
    tmpl.render()

if __name__ == '__main__':
    template_markdown()

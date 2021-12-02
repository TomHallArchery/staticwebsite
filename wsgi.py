import website
from website import create_app
from website.images.models import Img
from website.pages.models import Page
import config

app = create_app(config.DevConfig)


@app.shell_context_processor
def make_shell_context():
    return {
        'website': website,
        'db': website.db,
        'Img': Img,
        'Page': Page,
        'utils': website.utils,
        }


if __name__ == '__main__':
    app.run()

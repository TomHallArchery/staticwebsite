import website
from website import create_app
from website.images.models import Image
from website.pages.models import Page
import config

app = create_app(config.DevConfig)


@app.shell_context_processor
def make_shell_context():
    return {
        'website': website,
        'db': website.db,
        'Image': Image,
        'Page': Page,
        'utils': website.utils,
        'page': Page.objects.first(),
        'image': Image.objects.first(),
        }


if __name__ == '__main__':
    app.run()

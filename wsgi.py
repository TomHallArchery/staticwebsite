import website
from website import create_app
import config

app = create_app(config.DevConfig)

with open('tmp/results.html') as f:
    html = f.read()


@app.shell_context_processor
def make_shell_context():
    return {
        'website': website,
        'db': website.db,
        'Img': website.models.Img,
        'images': website.images,
        'i': website.models.Img.objects.first(),
        'html': html,
        'utils': website.utils
        }


if __name__ == '__main__':
    app.run()

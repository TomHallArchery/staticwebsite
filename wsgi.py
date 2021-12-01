import website
from website import create_app
import config

app = create_app(config.DevConfig)


@app.shell_context_processor
def make_shell_context():
    return {
        'website': website,
        'db': website.db,
        'models': website.models,
        'images': website.images,
        'utils': website.utils,
        }


if __name__ == '__main__':
    app.run()

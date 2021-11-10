from website import create_app, images
import config

app = create_app()
app.config.from_object(config.DevConfig)


def process_all_images():
    ''' Create thumbnails of images in src folder '''
    print("Processing images")
    all_imgs = images.SourceImages()
    all_imgs.add_to_db()
    all_imgs.process(reprocess=app.config['REPROC_IMAGES'])


if __name__ == '__main__':
    process_all_images()

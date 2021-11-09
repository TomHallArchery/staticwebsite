from website import app, images
import config

app.config.from_object(config.RunConfig)


def process_all_images():
    print("Processing images")
    all_imgs = images.SourceImages()
    all_imgs.add_to_db()
    all_imgs.process(reprocess=app.config['REPROC_IMAGES'])


if __name__ == '__main__':
    process_all_images()

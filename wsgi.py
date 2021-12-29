import website

app = website.create_app()


@app.shell_context_processor
def make_shell_context():
    Image = website.images.models.Image
    Page = website.pages.models.Page

    return {
        'website': website,
        'db': website.db,
        'Image': Image,
        'Page': Page,
        'page': Page.objects.first(),
        'image': Image.objects.first(),
        }


if __name__ == '__main__':
    app.run()

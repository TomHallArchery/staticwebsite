from pathlib import Path

import bs4
import pytest
from urlpath import URL

from website import create_app
from website.images import services as sv
from website.images.models import Image

APP_IMG_DOMAINS = [
    URL('/static/img/out/'),
    URL('http://localhost:5003/'),
    URL('https://cdn.tomhallarchery.com'),
]


@pytest.fixture()
def app():
    return create_app()


@pytest.fixture()
def path():
    return Path('tmp/test.jpg')


class TestWriteSrc:

    # what i really want to test/vallidate is that config contains good values!
    @pytest.mark.parametrize('url, expected', [
        (APP_IMG_DOMAINS[0], URL('/static/img/out/test.jpg')),
        (APP_IMG_DOMAINS[1], URL('http://localhost:5003/test.jpg')),
        (APP_IMG_DOMAINS[2], URL('https://cdn.tomhallarchery.com/test.jpg')),
    ])
    def test_good_inputs(self, url, path, expected):
        """
        GIVEN a known valid URL and path to an image
        WHEN write_src is called
        THEN check the result is a valid url,
            that does not include the paths parents
            and does include a width descriptor

        url_prefix: valid if starts with / or a http scheme and ://. Trailing / required if no scheme present.
        path: valid if exists and has a suffix
        """
        assert Path(expected).suffix == path.suffix
        assert sv.write_src(url, path) == expected

    @pytest.mark.parametrize('url', [
        URL('static/img/out/'),  # relative url
        URL('ftp://example.com'),  # bad scheme
        # '/static/img/out/',  # not a URL object; handled by static typing
    ])
    def test_raises(self, url, path):
        """
        GIVEN an invalid url
        WHEN write_src is called
        THEN check a ValueError is raised
        """
        with pytest.raises(ValueError):
            sv.write_src(url, path)


class TestWriteSrcset:

    def test_good_inputs(self, path):
        """
        GIVEN a valid domain, path and list of widths
        WHEN write_srcset is called
        THEN check output is the expected srcset string
        """
        srcset = sv.write_srcset(URL('/domain/'), path, [0, 1, 10, 100, 1000, 10_000])
        assert srcset == "/domain/test_0.jpg 0w, /domain/test_1.jpg 1w, /domain/test_10.jpg 10w, /domain/test_100.jpg 100w, /domain/test_1000.jpg 1000w, /domain/test_10000.jpg 10000w"


class TestWriteSizes:

    # couldn't think of anything more creative than a working example
    def test_example(self):
        """
        GIVEN a known dictionary
        WHEN write_sizes is called
        THEN check output is the expected sizes string
        """

        sizes = sv.write_sizes({'min-width: 110ch': '60vw', None: '95vw'})
        assert sizes == "(min-width: 110ch) 60vw, 95vw"

    # other tests:
    # ensure requires dict keys are optional valid css media expressions
    # ensure requires dict values are optional valid css width units


@pytest.fixture()
def image():
    return Image(
        name='test.jpg',
        filepath='tmp/test.jpg',
        width=3000,
        height=2000,
        thumbnail_widths=[2000, 1600, 1200, 800, 400]
    )


@pytest.fixture()
def soup():
    return bs4.BeautifulSoup('''
    <!DOCTYPE html>
    <html lang="en" dir="ltr">
      <head>
        <meta charset="utf-8">
        <title></title>
      </head>
      <body>
        <section>
          <h1>Test</h1>
          <img class="other" src="other.jpg"/>
          <img class="display" src="test.jpg" sizes="100vw" data-responsive/>
          <p>Below Image body text</p>
        </section>
      </body>
    </html>''', "html.parser")


class TestSetImgTag:

    def test_example(self, soup, image):
        """
        GIVEN a mock image object and a html img tag
        WHEN set_img_tag is called
        THEN check output is the expected html img tag
            with adjusted src, srcset, width and height attributes
            and one <url><width> pair per thumbnail width on model
        """

        attrs = {'src', 'srcset', 'width', 'height', 'data-responsive'}

        image_tag = soup.select('.display')[0]
        sv.set_img_tag(image_tag, image, APP_IMG_DOMAINS[2])

        # check attributes are present

        assert attrs <= set(image_tag.attrs.keys())

        # check srcset has as many descriptors as there are widths on image model
        srcset = image_tag.attrs['srcset']
        assert len(srcset.split(',')) == len(image.thumbnail_widths)


class TestWrapPicture:

    def test_example(self, soup, image):
        """
        GIVEN some html in :soup: and an image object
        WHEN wrap_picture is called
        THEN check output is the expected html picture set with source tag(s)
            and that wrapping has not changed the order of images
            and that only one image has been wrapped
            and that the images class has been transfered to the picture
        """
        image_tag = soup.select('.display')[0]

        sv.wrap_picture(soup, image_tag, image, APP_IMG_DOMAINS[2])
        # check only 1 picture has been wrapped
        assert len(soup.select('picture')) == 1
        # check picture now has imgs class
        assert "display" in soup.select('picture')[0]['class']

        # check n image formats added relates to model
        assert len(soup.select('source')) == max(1, len(image.formats) - 1)

        all_tags = soup.find_all()
        other_img = soup.find(class_="other")

        # given order in fixture, check image tag still comes after other img
        assert all_tags.index(image_tag) > all_tags.index(other_img)

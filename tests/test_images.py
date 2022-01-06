from pathlib import Path

from urlpath import URL
import pytest

# from website.images.models import Image
from website.images import services as sv

APP_IMG_DOMAINS = [
    URL('/static/img/out/'),
    URL('http://localhost:5003/'),
    URL('https://cdn.tomhallarchery.com'),
]


@pytest.fixture()
def path():
    return Path('tmp/test.jpg')


class TestWriteSrc():

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


class TestWriteSrcset():

    def test_good_inputs(self, path):
        """
        GIVEN a valid domain, path and list of widths
        WHEN write_srcset is called
        THEN check output is the expected srcset string
        """
        srcset = sv.write_srcset(URL('/domain/'), path, [0, 1, 10, 100, 1000, 10_000])
        assert srcset == "/domain/test_0.jpg 0w, /domain/test_1.jpg 1w, /domain/test_10.jpg 10w, /domain/test_100.jpg 100w, /domain/test_1000.jpg 1000w, /domain/test_10000.jpg 10000w"


class TestWriteSizes():

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

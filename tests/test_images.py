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


class TestWriteSrc():

    @pytest.fixture()
    def path(self):
        return Path('tmp/test.jpg')

    # what i really want to test/vallidate is that config contains good values!
    @pytest.mark.parametrize('url_prefix, expected', [
        (APP_IMG_DOMAINS[0], URL('/static/img/out/test.jpg')),
        (APP_IMG_DOMAINS[1], URL('http://localhost:5003/test.jpg')),
        (APP_IMG_DOMAINS[2], URL('https://cdn.tomhallarchery.com/test.jpg')),
    ])
    def test_good_inputs(self, url_prefix, path, expected):
        """
        GIVEN a known valid URL prefix and path to an image
        WHEN write_src is called
        THEN check the result is a valid url,
            that does not include the paths parents
            and does include a width descriptor

        url_prefix: valid if starts with / or a http scheme and ://. Trailing / required if no scheme present.
        path: valid if exists and has a suffix
        """
        assert Path(expected).suffix == path.suffix
        assert sv.write_src(url_prefix, path) == expected

    @pytest.mark.parametrize('url_prefix', [
        URL('static/img/out/'),  # relative url
        URL('ftp://example.com'),  # bad scheme
        # '/static/img/out/',  # not a URL object; handled by static typing
    ])
    def test_raises(self, url_prefix, path):
        """
        GIVEN an invalid url prefix
        WHEN write_src is called
        THEN check a ValueError is raised
        """
        with pytest.raises(ValueError):
            sv.write_src(url_prefix, path)

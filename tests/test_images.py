from pathlib import Path

import pytest

# from website.images.models import Image
from website.images import services as sv

USED_URL_PREFIXES = [
    '/static/img/out/',  # v
    'http://localhost:5003/',  # v
    'https://cdn.tomhallarchery.com',
]


class TestWriteSrc():

    @pytest.fixture()
    def path(self):
        return Path('tmp/test.jpg')

    # what i really want to test/vallidate is that config contains good values!
    @pytest.mark.parametrize('url_prefix, expected', [
        ('/static/img/out/', '/static/img/out/test.jpg'),
        ('http://localhost:5003', 'http://localhost:5003/test.jpg'),
        ('https://cdn.tomhallarchery.com', 'https://cdn.tomhallarchery.com/test.jpg'),
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
        assert sv.write_src(url_prefix, path) == expected
        assert Path(expected).suffix == path.suffix

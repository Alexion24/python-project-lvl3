import os
import requests
import tempfile
from page_loader.page_loader import download


HEXLET_URL = 'https://ru.hexlet.io/courses'
RU_HEXLET_IO_COURSES_HTML = os.path.join(
    'tests', 'fixtures', 'ru-hexlet-io-courses.html'
)


def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def test_download(requests_mock):
    with tempfile.TemporaryDirectory() as tmpdir:
        file_data = read_file(RU_HEXLET_IO_COURSES_HTML)
        requests_mock.get(HEXLET_URL, text=file_data)
        assert download(HEXLET_URL, tmpdir) == \
               os.path.join(tmpdir, 'ru-hexlet-io-courses.html')
        assert file_data == requests.get(HEXLET_URL).text

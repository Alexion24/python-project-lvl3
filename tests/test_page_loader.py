import os
import requests
import tempfile
from page_loader.page_loader import download


HEXLET_URL = 'https://page-loader.hexlet.repl.co'
HTML_FIXTURE = os.path.join(
    'tests', 'fixtures', 'page-loader-hexlet-repl-co.html'
)


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def test_download(requests_mock):
    with tempfile.TemporaryDirectory() as tmpdir:
        file_data = read_file(HTML_FIXTURE)
        requests_mock.get(HEXLET_URL, text=file_data)
        assert download(HEXLET_URL, tmpdir) == \
               os.path.join(tmpdir, 'page-loader-hexlet-repl-co.html')
        assert file_data == requests.get(HEXLET_URL).text

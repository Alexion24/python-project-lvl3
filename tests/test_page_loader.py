import os
import tempfile
from page_loader.page_loader import download


URL = 'https://page-loader.hexlet.repl.co'
IMAGE_URL = 'https://page-loader.hexlet.repl.co/assets/professions/nodejs.png'
HTML_PAGE_NAME = 'page-loader-hexlet-repl-co.html'
ORIGINAL_PAGE = os.path.join(
    'tests', 'fixtures', 'original_page.html'
)
DOWNLOADED_PAGE = os.path.join(
    'tests', 'fixtures', 'downloaded_page.html'
)
IMAGE_FIXTURE = os.path.join(
    'tests', 'fixtures', 'nodejs.png'
)
IMAGE_PATH = 'page-loader-hexlet-repl-co_files/' \
             'page-loader-hexlet-repl-co-assets-professions-nodejs.png'


def read_file(file_path, mode='r'):
    with open(file_path, mode) as file:
        return file.read()


def test_download(requests_mock):
    with tempfile.TemporaryDirectory() as tmpdir:
        requests_mock.get(URL, text=read_file(ORIGINAL_PAGE))
        requests_mock.get(IMAGE_URL, content=read_file(IMAGE_FIXTURE, 'rb'))
        download(URL, tmpdir)
        result_file = os.path.join(tmpdir, HTML_PAGE_NAME)
        result_png = os.path.join(tmpdir, IMAGE_PATH)
        assert read_file(result_file) == read_file(DOWNLOADED_PAGE)
        # assert read_file(result_png, 'rb') == read_file(IMAGE_FIXTURE, 'rb')

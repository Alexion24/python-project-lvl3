import os
import tempfile
from page_loader.page_loader import download


URL = 'https://ru.hexlet.io/courses'
IMAGE_URL = 'https://ru.hexlet.io/assets/professions/nodejs.png'
CSS_URL = 'https://ru.hexlet.io/assets/application.css'
SCRIPT_URL = 'https://ru.hexlet.io/packs/js/runtime.js'
HTML_PAGE_NAME = 'ru-hexlet-io-courses.html'
INNER_HTML_PAGE_NAME = 'ru-hexlet-io-courses.html'
ORIGINAL_PAGE_FIXTURE = os.path.join(
    'tests', 'fixtures', 'original_page.html'
)
DOWNLOADED_PAGE_FIXTURE = os.path.join(
    'tests', 'fixtures', 'downloaded_page.html'
)
INNER_HTML_FIXTURE = os.path.join(
    'tests', 'fixtures', 'inner_html.html'
)
IMAGE_FIXTURE = os.path.join(
    'tests', 'fixtures', 'nodejs.png'
)
CSS_FIXTURE = os.path.join(
    'tests', 'fixtures', 'css_file.css'
)
SCRIPT_FIXTURE = os.path.join(
    'tests', 'fixtures', 'script.js'
)
IMAGE_PATH = \
    'ru-hexlet-io-courses_files/ru-hexlet-io-assets-professions-nodejs.png'
INNER_HTML_PATH = 'ru-hexlet-io-courses_files/ru-hexlet-io-courses.html'
CSS_PATH = 'ru-hexlet-io-courses_files/ru-hexlet-io-assets-application.css'
SCRIPT_PATH = 'ru-hexlet-io-courses_files/ru-hexlet-io-packs-js-runtime.js'


def read_file(file_path, mode='r'):
    with open(file_path, mode) as file:
        return file.read()


def test_download(requests_mock):
    with tempfile.TemporaryDirectory() as tmpdir:
        requests_mock.get(URL, text=read_file(ORIGINAL_PAGE_FIXTURE))
        requests_mock.get(IMAGE_URL, content=read_file(IMAGE_FIXTURE, 'rb'))
        requests_mock.get(URL, text=read_file(INNER_HTML_FIXTURE))
        requests_mock.get(CSS_URL, text=read_file(CSS_FIXTURE))
        requests_mock.get(SCRIPT_URL, text=read_file(SCRIPT_FIXTURE))
        download(URL, tmpdir)
        result_html = os.path.join(tmpdir, HTML_PAGE_NAME)
        result_png = os.path.join(tmpdir, IMAGE_PATH)
        result_inner_html = os.path.join(tmpdir, INNER_HTML_PATH)
        result_css = os.path.join(tmpdir, CSS_PATH)
        result_script = os.path.join(tmpdir, SCRIPT_PATH)
        assert read_file(result_html) == read_file(DOWNLOADED_PAGE_FIXTURE)
        assert read_file(result_png, 'rb') == read_file(IMAGE_FIXTURE, 'rb')
        assert read_file(result_inner_html) == read_file(INNER_HTML_FIXTURE)
        assert read_file(result_css) == read_file(CSS_FIXTURE)
        assert read_file(result_script) == read_file(SCRIPT_FIXTURE)

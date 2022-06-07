import os
import tempfile
import pytest
import requests
from page_loader.page_loader import download
from page_loader.data_handler import get_data_from_url, save_data_to_file
from page_loader.url_handler import get_directory_name, get_html_file_name
from urllib.parse import urljoin


URL = 'https://ru.hexlet.io/courses'
IMAGE_URL = 'https://ru.hexlet.io/assets/professions/nodejs.png'
CSS_URL = 'https://ru.hexlet.io/assets/application.css'
SCRIPT_URL = 'https://ru.hexlet.io/packs/js/runtime.js'
DIRECTORY_NAME = 'ru-hexlet-io-courses_files'
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
ERRORS = [
    requests.exceptions.RequestException,
    requests.exceptions.HTTPError,
    requests.exceptions.Timeout
]


def read_file(file_path, mode='r'):
    with open(file_path, mode) as file:
        return file.read()


def test_get_directory_name():
    correct_answer = DIRECTORY_NAME
    result_directory_name = get_directory_name(URL)
    assert result_directory_name == correct_answer


def test_get_html_file_name():
    correct_answer = HTML_PAGE_NAME
    result_page_name = get_html_file_name(URL)
    assert result_page_name == correct_answer


def test_save_data_to_file(requests_mock):
    with tempfile.TemporaryDirectory() as tmpdir:
        correct_answer = read_file(ORIGINAL_PAGE_FIXTURE)
        requests_mock.get(URL, text=correct_answer)
        data_from_url = get_data_from_url(URL)
        file_path = os.path.join(tmpdir, HTML_PAGE_NAME)
        save_data_to_file(file_path, data_from_url)
        result = read_file(file_path)
        assert result == correct_answer


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


@pytest.mark.parametrize('error', ERRORS)
def test_response_with_http_error(requests_mock, error):
    with tempfile.TemporaryDirectory() as tmpdir:
        requests_mock.get(URL, exc=error)
        requests_mock.get(URL, exc=error)
        requests_mock.get(URL, exc=error)
        with pytest.raises(error):
            assert not download(URL, tmpdir)


def test_response_with_error(requests_mock):
    with tempfile.TemporaryDirectory() as tmpdir:
        url1 = urljoin(URL, '403')
        url2 = urljoin(URL, '404')
        url3 = urljoin(URL, '500')
        requests_mock.get(url1, status_code=403)
        requests_mock.get(url2, status_code=404)
        requests_mock.get(url3, status_code=500)
        with pytest.raises(Exception):
            assert download(url1, tmpdir)
            assert download(url2, tmpdir)
            assert download(url3, tmpdir)


def test_save_to_file_with_permission_error(requests_mock):
    requests_mock.get(URL, text=read_file(ORIGINAL_PAGE_FIXTURE))
    data_from_url = get_data_from_url(URL)
    file_path = '/random_file_path'
    with pytest.raises(PermissionError):
        save_data_to_file(file_path, data_from_url)


def test_directory_not_exist():
    with tempfile.TemporaryDirectory() as tmpdir:
        not_exists_directory = os.path.join(tmpdir, 'random_dir_name')
        with pytest.raises(OSError):
            download(URL, not_exists_directory)

import os
from page_loader.file_handler import save_html_to_file
from page_loader.url_handler import get_html_file_name, get_data_from_url
from urllib.parse import urlparse


DEFAULT_DIR = os.getcwd()


def download(url, file_path=DEFAULT_DIR):
    parsed_url = urlparse(url)
    parsed_path = f'{parsed_url.netloc}{parsed_url.path}'
    result_string = get_html_file_name(parsed_path)
    result_file_path = os.path.join(file_path, result_string)
    data_from_url = get_data_from_url(url)
    save_html_to_file(result_file_path, data_from_url)
    return result_file_path

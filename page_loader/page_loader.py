import os
import requests
from urllib.parse import urlparse


DEFAULT_DIR = os.getcwd()


def download(url, file_path=DEFAULT_DIR):
    parsed_url = urlparse(url)
    parsed_path = f'{parsed_url.netloc}{parsed_url.path}'
    result_string = ''
    for symbol in parsed_path:
        if not symbol.isalnum():
            result_string += '-'
        else:
            result_string += symbol
    result_string += '.html'
    result_file_path = os.path.join(file_path, result_string)
    with open(result_file_path, 'w') as file:
        file.write(get_data_from_url(url))
    return result_file_path


def get_data_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    raise Exception('Connection problem or incorrect url')

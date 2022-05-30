import requests
from page_loader.url_handler import get_absolute_url


def get_data_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    raise Exception('Connection problem or incorrect url')


def get_data_from_resource(url, resource):
    link = get_absolute_url(url, resource)
    return get_data_from_url(link)


def save_data_to_file(file_path, data):
    mode = 'wb+' if isinstance(data, bytes) else 'w'
    with open(file_path, mode) as file:
        file.write(data)

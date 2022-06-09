import logging
import requests
from page_loader.url_handler import get_absolute_url


def get_data_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        logging.error(error)
        raise f'Connection failed. Status code: {requests.get(url).status_code}'
    return response.content


def get_data_from_resource(url, resource):
    link = get_absolute_url(url, resource)
    return get_data_from_url(link)


def save_data_to_file(file_path, data):
    mode = 'wb+' if isinstance(data, bytes) else 'w'
    try:
        with open(file_path, mode) as file:
            file.write(data)
    except PermissionError as error:
        logging.error(f'Access denied to file {file_path}')
        raise error
    except OSError as error:
        logging.error(f'Unable to save to file {file_path}')
        raise error

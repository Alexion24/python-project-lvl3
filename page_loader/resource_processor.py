import logging
import os
import requests
from pathlib import Path
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from progress.bar import ChargingBar
from page_loader.data_saver import save_data_to_file
from page_loader.url_handler import is_url_local, adapt_string, \
    get_url_string_name, get_resource_directory_name, get_right_url_structure, \
    get_absolute_url


TAG_ATTRIBUTES = {'img': 'src', 'link': 'href', 'script': 'src'}


def get_data_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        logging.error(error)
        raise f'Connection failed. Status code: {requests.get(url).status_code}'
    return response.content


def get_link_from_tag(resource):
    if 'link' in str(resource):
        return resource.get('href')
    elif 'img' in str(resource) or 'script' in str(resource):
        return resource.get('src')


def get_data_from_resource(url, resource):
    link = get_absolute_url(url, resource)
    return get_data_from_url(link)


def get_resource_name(url, resource):
    parsed_resource = urlparse(resource)
    if Path(resource).suffix:
        src = resource[:-len(Path(resource).suffix)]
        suffix = Path(resource).suffix
    else:
        src = resource
        suffix = '.html'
    if parsed_resource.scheme:
        src = src[len(parsed_resource.scheme) + 3:]
        name = adapt_string(src)
        resource_name = name + suffix
    else:
        name = adapt_string(src)
        resource_name = get_url_string_name(url) + name + suffix
    return resource_name


def get_content_and_resources(url, data_from_url):
    soup = BeautifulSoup(data_from_url, 'html.parser')
    logging.debug('Parsing web page content...')
    tags = list(TAG_ATTRIBUTES.keys())
    resource_tags = soup.find_all(tags)
    right_structure_url = get_right_url_structure(url)
    paths_to_links = {}
    for resource_tag in resource_tags:
        link = get_link_from_tag(resource_tag)
        if is_url_local(link, url):
            file_name = get_resource_name(right_structure_url, link)
            path_to_link = f'{get_resource_directory_name(url)}/{file_name}'
            resource_tag[TAG_ATTRIBUTES[resource_tag.name]] = path_to_link
            paths_to_links[link] = path_to_link
    result_content = soup.prettify()
    logging.debug('Changed web page content received.')
    return result_content, paths_to_links


def create_directory(resources_path):
    try:
        os.mkdir(resources_path)
    except FileNotFoundError as error:
        print(f'No such file or directory: {resources_path}.')
        logging.exception(f'No such file or directory: {resources_path}.')
        raise error
    except OSError as error:
        print(f'Directory {resources_path} already exists.')
        logging.exception(f'Directory {resources_path} already exists.')
        raise error


def download_resources(url, directory_path, paths_to_links):
    directory_with_resources = get_resource_directory_name(url)
    resources_path = os.path.join(directory_path, directory_with_resources)
    logging.info(f'Downloaded files will be saved in {resources_path}.')
    create_directory(resources_path)
    for link, path in paths_to_links.items():
        right_structure_url = get_right_url_structure(url)
        logging.debug(f'Downloading {right_structure_url + link}')
        file_name = get_resource_name(right_structure_url, link)
        file_path = os.path.join(resources_path, file_name)
        bar = ChargingBar(
            f'Downloading: | {file_name} |',
            max=1,
            suffix='%(percent)d%%'
        )
        try:
            resource_data = get_data_from_resource(
                right_structure_url,
                link
            )
            save_data_to_file(file_path, resource_data)
            logging.debug(
                f'Data from {right_structure_url + link} successfully saved'
            )
            bar.next()
        except PermissionError as error:
            logging.error(f'Access denied to file {file_path}')
            raise error
        except requests.RequestException as error:
            logging.info(error)
            logging.warning(f'Unable to handle {link}')
            continue
        except OSError as error:
            logging.error(f'Unable to save data to {file_path}')
            raise error
        bar.finish()

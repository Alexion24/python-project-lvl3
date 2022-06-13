import logging
import os
import requests
from pathlib import Path
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from progress.bar import ChargingBar
from page_loader.data_saver import save_data_to_file
from page_loader.url_handler import is_url_local, adapt_string, \
    get_url_string_name, get_directory_name, get_right_url_structure, \
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
    for key, value in TAG_ATTRIBUTES.items():
        if key in str(resource):
            return resource.get(value)


def get_resources(resource_tags, url):
    link_from_tag = {}
    for resource in resource_tags:
        link = get_link_from_tag(resource)
        if is_url_local(link, url):
            link_from_tag[resource] = link
    return link_from_tag


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


def download_resources(url, directory_path, resource_paths):
    paths_to_links = []
    for resource in resource_paths:
        right_structure_url = get_right_url_structure(url)
        logging.debug(f'Downloading {right_structure_url + resource}')
        file_name = get_resource_name(right_structure_url, resource)
        file_path = os.path.join(directory_path, file_name)
        bar = ChargingBar(
            f'Downloading: | {file_name} |',
            max=1,
            suffix='%(percent)d%%'
        )
        try:
            resource_data = get_data_from_resource(
                right_structure_url,
                resource
            )
            save_data_to_file(file_path, resource_data)
            bar.next()
        except PermissionError as error:
            logging.error(f'Access denied to file {file_path}')
            raise error
        except requests.RequestException as error:
            logging.info(error)
            logging.warning(f'Unable to handle {resource}')
            continue
        except OSError as error:
            logging.error(f'Unable to save data to {file_path}')
            raise error
        path_to_link = f'{get_directory_name(url)}/{file_name}'
        bar.next()
        paths_to_links.append(path_to_link)
        bar.finish()
    return paths_to_links


def change_resource_paths(link_from_tag, paths_to_links):
    for tag, local_file_link in zip(link_from_tag.keys(), paths_to_links):
        tag[TAG_ATTRIBUTES[tag.name]] = local_file_link


def get_changed_data(url, data_from_url, resources_path):
    soup = BeautifulSoup(data_from_url, 'html.parser')
    logging.debug('Parsing web page content...')
    tags = list(TAG_ATTRIBUTES.keys())
    resource_tags = soup.find_all(tags)
    link_from_tag = get_resources(resource_tags, url)
    paths_to_links = download_resources(
        url,
        resources_path,
        link_from_tag.values()
    )
    change_resource_paths(link_from_tag, paths_to_links)
    result_content = soup.prettify()
    return result_content


def get_result_page_content(url, resources_path):
    data_from_url = get_data_from_url(url)
    logging.debug('Web page content received.')
    result_content = get_changed_data(url, data_from_url, resources_path)
    logging.debug('Changed web page content received.')
    return result_content

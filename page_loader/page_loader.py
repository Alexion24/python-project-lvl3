import logging
import os
from bs4 import BeautifulSoup
from page_loader.data_handler import save_data_to_file, get_data_from_url
from page_loader.url_handler import get_html_file_name, get_directory_name
from page_loader.resources_handler import handling_resources


DEFAULT_DIR = os.getcwd()
TAGS = ['img', 'link', 'script']


def download(url, directory_path=DEFAULT_DIR):
    data_from_url = get_data_from_url(url)
    logging.debug('Web page content received.')
    result_file_name = get_html_file_name(url)
    result_file_path = os.path.join(directory_path, result_file_name)
    logging.info(
        f'Web page {url} content will be downloaded in {result_file_path}.'
    )
    directory_with_resources = get_directory_name(url)
    resources_path = os.path.join(directory_path, directory_with_resources)
    os.mkdir(resources_path)
    logging.info(f'Downloaded files will be saved in {resources_path}.')
    soup = BeautifulSoup(data_from_url, 'html.parser')
    logging.debug('Parsing web page content...')
    resource_tags = soup.find_all(TAGS)
    logging.debug('Downloading web page content...')
    handling_resources(url, resources_path, resource_tags)
    logging.info('Web page content successfully downloaded.')
    save_data_to_file(result_file_path, soup.prettify())
    logging.info(f'Web page content successfully saved in {result_file_path}.')
    return result_file_path

import logging
import os
from page_loader.data_saver import save_data_to_file
from page_loader.url_handler import get_html_file_name, get_directory_name
from page_loader.resource_processor import get_content_and_resources, \
    download_resources, get_data_from_url

DEFAULT_DIR = os.getcwd()


def download(url, directory_path=DEFAULT_DIR):
    result_file_name = get_html_file_name(url)
    result_file_path = os.path.join(directory_path, result_file_name)
    logging.info(
        f'Web page {url} content will be downloaded in {result_file_path}.'
    )
    data_from_url = get_data_from_url(url)
    logging.debug('Web page content received.')
    result_content, paths_to_links = get_content_and_resources(
        url,
        data_from_url
    )
    logging.debug('Downloading web page content...')
    directory_with_resources = get_directory_name(url)
    resources_path = os.path.join(directory_path, directory_with_resources)
    logging.info(f'Downloaded files will be saved in {resources_path}.')
    download_resources(url, resources_path, paths_to_links)
    logging.info('Web page content successfully downloaded.')
    save_data_to_file(result_file_path, result_content)
    logging.info(f'Web page content successfully saved in {result_file_path}.')
    return result_file_path

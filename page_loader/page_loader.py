import logging
import os
from page_loader.data_saver import save_data_to_file
from page_loader.url_handler import get_html_file_name, get_directory_name
from page_loader.resource_processor import get_result_page_content


DEFAULT_DIR = os.getcwd()


def download(url, directory_path=DEFAULT_DIR):
    result_file_name = get_html_file_name(url)
    result_file_path = os.path.join(directory_path, result_file_name)
    logging.info(
        f'Web page {url} content will be downloaded in {result_file_path}.'
    )
    logging.debug('Downloading web page content...')
    directory_with_resources = get_directory_name(url)
    resources_path = os.path.join(directory_path, directory_with_resources)
    logging.info(f'Downloaded files will be saved in {resources_path}.')
    result_content = get_result_page_content(url, resources_path)
    logging.info('Web page content successfully downloaded.')
    save_data_to_file(result_file_path, result_content)
    logging.info(f'Web page content successfully saved in {result_file_path}.')
    return result_file_path

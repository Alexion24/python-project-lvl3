import os
from bs4 import BeautifulSoup
from page_loader.data_handler import save_data_to_file, get_data_from_url
from page_loader.url_handler import get_html_file_name, get_url_string_name, \
    get_directory_name
from page_loader.resources_handler import handling_resources


DEFAULT_DIR = os.getcwd()
TAGS = ['img', 'link', 'script']


def download(url, directory_path=DEFAULT_DIR):
    url_string_name = get_url_string_name(url)
    result_file_name = get_html_file_name(url_string_name)
    result_file_path = os.path.join(directory_path, result_file_name)
    data_from_url = get_data_from_url(url)
    directory_with_resources = get_directory_name(url)
    resources_path = os.path.join(directory_path, directory_with_resources)
    os.mkdir(resources_path)
    soup = BeautifulSoup(data_from_url, 'html.parser')
    resource_tags = soup.find_all(TAGS)
    handling_resources(url, resources_path, resource_tags)
    save_data_to_file(result_file_path, soup.prettify())
    return result_file_path

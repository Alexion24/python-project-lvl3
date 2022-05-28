import requests


def get_data_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    raise Exception('Connection problem or incorrect url')


def get_html_file_name(file_path):
    result_file_name = ''
    for symbol in file_path:
        if not symbol.isalnum():
            result_file_name += '-'
        else:
            result_file_name += symbol
    return result_file_name + '.html'

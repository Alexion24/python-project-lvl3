from urllib.parse import urlparse, urljoin


def adapt_string(string):
    result_string = ''
    for symbol in string:
        if not symbol.isalnum():
            result_string += '-'
        else:
            result_string += symbol
    return result_string


def get_url_string_name(url):
    parsed_url = urlparse(url)
    parsed_path = f'{parsed_url.netloc}{parsed_url.path}'
    return adapt_string(parsed_path)


def get_downloaded_file_name(url):
    parsed_url = urlparse(url)
    return adapt_string(parsed_url)


def get_directory_name(url):
    return get_url_string_name(url) + '_files'


def get_html_file_name(url):
    return get_url_string_name(url) + '.html'


def get_right_url_structure(url):
    parsed_url = urlparse(url)
    return parsed_url.scheme + '://' + parsed_url.netloc


def is_url_local(url, resource_url):
    parsed_url = urlparse(url)
    resource_url_netloc = urlparse(resource_url).netloc
    return parsed_url.netloc == '' or parsed_url.netloc == resource_url_netloc


def get_absolute_url(root_page_url, url):
    if not urlparse(url).netloc:
        return urljoin(root_page_url, url)
    else:
        return url

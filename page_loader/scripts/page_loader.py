import argparse
import logging
import sys

from page_loader.page_loader import download


LOG_FILE = 'page_loader.log'


def main():
    parser = argparse.ArgumentParser(
        usage='page-loader [-h] [-o OUTPUT] url',
        description='Download html page'
    )
    parser.add_argument('url')
    parser.add_argument(
        '-o', '--output',
        help='set output directory'
    )
    args = parser.parse_args()
    try:
        file_path = download(args.url, args.output)
    except Exception as error:
        logging.error(error)
        print(f'Unexpected error! For additional info see {LOG_FILE}.')
        sys.exit(1)
    else:
        message = f'Page successfully downloaded into {file_path}'
        print(message)
        logging.info(message)
        sys.exit(0)


if __name__ == '__main__':
    main()

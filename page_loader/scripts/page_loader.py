import argparse
from page_loader.page_loader import download


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
    print(download(args.url, args.output))


if __name__ == '__main__':
    main()

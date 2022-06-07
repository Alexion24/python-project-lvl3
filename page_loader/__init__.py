import logging
from page_loader.page_loader import download


__all__ = ('download', )

FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_FILE = 'page_loader.log'

logging.basicConfig(
    filename=LOG_FILE,
    filemode='w',
    format=FORMAT,
    level=logging.DEBUG
)

import logging


def save_data_to_file(file_path, data):
    mode = 'wb+' if isinstance(data, bytes) else 'w'
    try:
        with open(file_path, mode) as file:
            file.write(data)
    except PermissionError as error:
        logging.error(f'Access denied to file {file_path}')
        raise error
    except OSError as error:
        logging.error(f'Unable to save to file {file_path}')
        raise error

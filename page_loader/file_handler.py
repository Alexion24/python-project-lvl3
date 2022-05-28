def save_html_to_file(file_path, data):
    mode = 'wb+' if isinstance(data, bytes) else 'w'
    with open(file_path, mode) as file:
        file.write(data)

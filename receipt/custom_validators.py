def validate_file_extension(value):
    if value.content_type != 'text/plain':
        raise Exception('Only .txt files are allowed')

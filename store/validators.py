from django.core.exceptions import ValidationError

def validate_file_szie(file):
    max_size_kb = 50

    if file.size > max_size_kb * 1024:
        raise ValidationError(f'File can\'t be larger than {max_size_kb}KB')

import re
import unicodedata


def digits_only(value: str) -> str:
    return ''.join(filter(str.isdigit, value))


def slugify(value: str) -> str:
    value = unicodedata.normalize('NFKD', value)
    value = value.encode('ascii', 'ignore').decode('ascii')
    value = value.lower()
    value = re.sub(r'[^a-z0-9]+', '-', value)
    value = re.sub(r'-+', '-', value)
    value = value.strip('-')
    return value

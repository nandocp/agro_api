def digits_only(value: str) -> str:
    return ''.join(filter(str.isdigit, value))

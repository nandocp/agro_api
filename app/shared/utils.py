from pydantic import BaseModel


def sanitize_filters(filters: BaseModel) -> dict:
    filters_dict = filters.model_dump()
    for key in ['offset', 'limit']:
        filters_dict.pop(key, None)
    return {key: val for key, val in filters_dict.items() if val is not None}

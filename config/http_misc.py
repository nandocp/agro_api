from http import HTTPStatus
from typing import Annotated, Type, TypeVar

from fastapi import HTTPException, Query
from pydantic import BaseModel

FilterSchemaType = TypeVar('FilterSchemaType', bound=BaseModel)


def unauthorized(message='You shall not do it'):
    raise HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail=message,
    )


def unprocessable(message: str):
    raise HTTPException(
        status_code=HTTPStatus.UNPROCESSABLE_CONTENT,
        detail=message,
    )


def with_conflict(message: str = 'Action cannot be completed'):
    raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=message)


def not_found(message=''):
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=message)


def filters(filter_schema: Type[FilterSchemaType]):
    return Annotated[filter_schema, Query()]

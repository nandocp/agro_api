from http import HTTPStatus

from fastapi import HTTPException


def unauthorized():
    raise HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='You shall not do it',
    )


def unprocessable(message: str):
    raise HTTPException(
        status_code=HTTPStatus.UNPROCESSABLE_CONTENT,
        detail=message,
    )

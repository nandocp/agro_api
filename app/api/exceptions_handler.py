import re
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.shared.exceptions import AgroAPIError
from config.logging import logger
from config.settings import settings


def register_exception_handlers(app: FastAPI) -> None:
    def _status_for_code(exc_code: str) -> int:
        if exc_code.startswith('not_found'):
            return HTTPStatus.NOT_FOUND
        if exc_code.startswith('auth'):
            return HTTPStatus.UNAUTHORIZED
        if exc_code.startswith('quota'):
            return HTTPStatus.PAYMENT_REQUIRED
        if exc_code.startswith(('integrity_error', 'conflict')):
            return HTTPStatus.CONFLICT
        if exc_code.startswith('unprocessable'):
            return HTTPStatus.UNPROCESSABLE_ENTITY
        return HTTPStatus.INTERNAL_SERVER_ERROR

    @app.exception_handler(AgroAPIError)
    async def agro_api_error_handler(request: Request, exc: AgroAPIError):
        status = _status_for_code(exc.code)
        return JSONResponse(
            status_code=status,
            content={'code': exc.code, 'message': exc.message},
        )

    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        error_message = str(exc.orig)

        if settings.ENVIRONMENT != 'test':
            logger.error(exc)
        match = re.search(r'constraint "([^"]+)"', error_message)
        code = (
            f'integrity_error.{match.group(1)}'
            if match
            else 'integrity_error.generic'
        )

        return JSONResponse(
            status_code=HTTPStatus.CONFLICT,
            content={'code': code},
        )

    @app.exception_handler(Exception)
    async def generic_handler(request: Request, exc: Exception):
        logger.error(f'Unhandled exception: {exc}', exc_info=True)

        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={
                'code': 'error.internal',
                'message': 'Unexpected error',
            },
        )

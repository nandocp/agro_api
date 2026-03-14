from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, OperationalError

from app.shared.exceptions import (
    ConflictError,
    NotFoundError,
    QuotaExceededError,
    UnauthorizedError,
)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError):
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content={'detail': f'{exc.resource} not found'},
        )

    @app.exception_handler(UnauthorizedError)
    async def unauthorized_handler(request: Request, exc: UnauthorizedError):
        return JSONResponse(
            status_code=HTTPStatus.UNAUTHORIZED,
            content={'detail': exc.message},
        )

    @app.exception_handler(ConflictError)
    async def conflict_handler(request: Request, exc: ConflictError):
        return JSONResponse(
            status_code=HTTPStatus.CONFLICT,
            content={'detail': exc.message},
        )

    @app.exception_handler(QuotaExceededError)
    async def quota_handler(request: Request, exc: QuotaExceededError):
        return JSONResponse(
            status_code=HTTPStatus.PAYMENT_REQUIRED,
            content={'detail': exc.message},
        )

    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        return JSONResponse(
            status_code=HTTPStatus.CONFLICT,
            content={'detail': 'Operation conflicts with existing data'},
        )

    @app.exception_handler(OperationalError)
    async def operational_error_handler(
        request: Request, exc: OperationalError
    ):
        return JSONResponse(
            status_code=HTTPStatus.SERVICE_UNAVAILABLE,
            content={'detail': 'Service temporarily unavailable'},
        )

    @app.exception_handler(Exception)
    async def generic_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={'detail': 'An unexpected error occurred'},
        )

from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse

# from app.api.public.router import router as public_router
from app.api.auth.router import router as auth_router
from app.api.private.router import router as private_router
from config.authentication import get_current_user
from config.settings import settings

router = APIRouter()


@router.get('/', status_code=HTTPStatus.OK)
def root():
    return {'message': 'AgroAPI', 'version': settings.VERSION}


@router.get('/up', status_code=HTTPStatus.OK)
def up():
    return {'message': 'ok'}


@router.get('/html', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def html():
    return """<html>
        <head>AgroAPI</head>
        <body>🚜</body>
    </html>"""


router.include_router(auth_router, prefix='/auth')
# router.include_router(public_router, prefix='/public')
router.include_router(
    private_router, prefix='/api', dependencies=[Depends(get_current_user)]
)

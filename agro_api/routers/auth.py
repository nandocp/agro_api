from fastapi import APIRouter
from http import HTTPStatus

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/login', status_code=HTTPStatus.NO_CONTENT)
def login():
    pass

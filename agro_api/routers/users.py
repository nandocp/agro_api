from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from agro_api.schemas.user import UserPostPayloadSchema, UserPostResponseSchema
from agro_api.services.user import UserService
from config.database import get_session

router = APIRouter(prefix='/users', tags=['users'])
session = Annotated[Session, Depends(get_session)]


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=UserPostResponseSchema
)
def create(user: UserPostPayloadSchema, session: session):
    response = UserService(session).create(user)

    if isinstance(response, dict):
        raise HTTPException(**response)

    return response


# def show(user_id: str, session: Session=Depends(get_session)):

# def index():

# def update():

# def delete():

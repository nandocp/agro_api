from fastapi import APIRouter

from agro_api.schemas.estate import EstatePostPayloadSchema

router = APIRouter(prefix='/estates', tags=['estates'])


@router.post('/', response_model=EstatePostPayloadSchema)
def create():
    pass

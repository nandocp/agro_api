from http import HTTPStatus

from fastapi import APIRouter

from agro_api.endpoints.estates import estates as estates_endpoints
from agro_api.schemas.estate import EstateItem, EstatesList

router = APIRouter(prefix='/estates', tags=['estates'])

router.add_api_route(
    '/',
    estates_endpoints.get_estates,
    methods=['GET'],
    response_model=EstatesList,
    status_code=HTTPStatus.OK,
    summary='Get Estates',
    description='Get Estates with filters and pagination',
)

router.add_api_route(
    '/',
    estates_endpoints.create_estate,
    methods=['POST'],
    response_model=EstateItem,
    status_code=HTTPStatus.CREATED,
    summary='Create Estate',
)

router.add_api_route(
    '/{id}',
    estates_endpoints.get_estate,
    methods=['GET'],
    response_model=EstateItem,
    status_code=HTTPStatus.OK,
    summary='Get a single Estate data',
)

router.add_api_route(
    '/{id}',
    estates_endpoints.update_estate,
    methods=['PUT', 'POST'],
    response_model=EstateItem,
    status_code=HTTPStatus.OK,
    summary='Update Estate',
)

# @router.post('/', response_model=EstateItem, status_code=HTTPStatus.CREATED)
# async def create(session: session, user: current_user, estate: EstateBase):
#     try:
#         service = await EstateService(session, user).create(estate)
#     except IntegrityError:
#         raise HTTPException(
#             status_code=HTTPStatus.UNPROCESSABLE_CONTENT,
#             detail='Slug already exists',
#         )

#     return service


# @router.get('/', response_model=EstatesList, status_code=HTTPStatus.OK)
# async def index(session: session, user: current_user, filters: filters):
#     return await EstateService(session, user).get_many(filters)


# @router.get('/{estate_id}', response_model=EstateItem)
# async def show(session: session, user: current_user, estate_id: str):
#     estate = await EstateService(session, user).get_one(estate_id)

#     if not estate:
#         raise HTTPException(
#             status_code=HTTPStatus.NOT_FOUND, detail='Estate not found'
#         )

#     return estate


# @router.put('/{estate_id}', response_model=EstateItem)
# async def update(
#     params: EstateBase, user: current_user, estate_id: str, session: session
# ):
#     try:
#         estate = await EstateService(session, user).update(estate_id, params)
#     except IntegrityError:
#         raise HTTPException(
#             status_code=HTTPStatus.UNPROCESSABLE_CONTENT,
#             detail='Slug already exists',
#         )

#     if not estate:
#         raise HTTPException(
#             status_code=HTTPStatus.NOT_FOUND, detail='Estate not found'
#         )

#     return estate

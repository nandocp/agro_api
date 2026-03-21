# tests/domain/estates/conftest.py
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.estates.enums import EstateZone, OwnershipType
from app.domain.estates.schemas.estate import EstateCreate
from app.domain.estates.services.estate import EstateService

VALID_BOUNDARY = (
    'MULTIPOLYGON ((('
    '-45.8923 -21.7342, '
    '-45.8745 -21.7342, '
    '-45.8621 -21.7428, '
    '-45.8512 -21.7584, '
    '-45.8478 -21.7741, '
    '-45.8523 -21.7895, '
    '-45.8656 -21.7982, '
    '-45.8842 -21.8015, '
    '-45.8978 -21.7956, '
    '-45.9034 -21.7832, '
    '-45.9021 -21.7654, '
    '-45.8967 -21.7512, '
    '-45.8923 -21.7342'
    ')))'
)

OVERLAPPING_BOUNDARY_WKT = (
    'MULTIPOLYGON ((('
    '-45.8800 -21.7342, '  # começa dentro do DEFAULT_BOUNDARY
    '-45.8600 -21.7342, '
    '-45.8500 -21.7428, '
    '-45.8400 -21.7584, '
    '-45.8800 -21.7584, '
    '-45.8800 -21.7342'
    ')))'
)

VALID_ENTRANCE_POINT = 'POINT (-45.8800 -21.7600)'


@pytest.fixture
def estate_create_data() -> dict:
    return {
        'label': 'Fazenda São João',
        'slug': 'fazenda-sao-joao',
        'description': 'Test estate',
        'timezone': 'America/Sao_Paulo',
        'zone': EstateZone.RURAL,
        'ownership_type': OwnershipType.OWNED,
        'boundary_wkt': VALID_BOUNDARY,
        'entrance_point_wkt': VALID_ENTRANCE_POINT,
    }


@pytest.fixture
def estate_create(estate_create_data) -> EstateCreate:
    return EstateCreate(**estate_create_data)


@pytest_asyncio.fixture
async def estate_service(session: AsyncSession) -> EstateService:
    return EstateService(session)

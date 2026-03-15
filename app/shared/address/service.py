from uuid import UUID

from app.shared.address.model import Address
from app.shared.address.schemas import AddressCreate, AddressUpdate
from app.shared.service import BaseService


class AddressService(BaseService[Address, AddressCreate, AddressUpdate]):
    async def create_or_update(
        self,
        address_id: UUID | None,
        data: AddressCreate,
    ) -> Address:
        if address_id:
            existing = await self.repo.get_one(address_id)
            if existing:
                return await self.repo.update(existing, data)
        return await self.repo.create(data)

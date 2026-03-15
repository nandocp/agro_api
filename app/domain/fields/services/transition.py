# FieldTransition só para SPLIT e MERGE — sempre tem predecessor e successor
# para realizar transição, utilizar permissão
# DEACTIVATE apenas para manager e admin

# Field1 (x subdividido em 2)
#   |__ Field2 --> (FieldTransition successor: Field2, predecessor: Field1)
#   |__ Field3 --> (FieldTransition successor: Field3, predecessor: Field1)

from app.domain.fields.models import FieldTransition
from app.shared.service import BaseService


class FieldTransitionService(BaseService[FieldTransition]):
    pass


# async def split_field(
#     self,
#     field_id: UUID,
#     successors_data: list[FieldCreate],
#     current_user: User,
# ) -> list[Field]:
#     predecessor = await self.repo.get_one(field_id)
#     if not predecessor:
#         raise NotFoundError('field')

#     # desativa o predecessor
#     predecessor.active_to = date.today()
#     await self.repo.save(predecessor)

#     # cria successors e transitions
#     successors = []
#     for data in successors_data:
#         successor = await self.repo.create(data)
#         await self.transition_repo.create(
#             FieldTransitionCreate(
#                 predecessor_id=predecessor.id,
#                 successor_id=successor.id,
#                 transition_type=FieldTransitionType.DIVIDE,
#                 transitioned_by_id=current_user.id,
#             )
#         )
#         successors.append(successor)

#     await self.events.publish(
#         FieldEventCreator.field_divided(
#             predecessor, successors, current_user.id
#         )
#     )
#     return successors

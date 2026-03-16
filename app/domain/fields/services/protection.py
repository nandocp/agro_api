# # service verifica o kind para determinar o que está bloqueado
# PROTECTION_BLOCKS = {
#     'environmental': ['deletion', 'transition', 'boundary_change'],
#     'embargo': ['deletion', 'transition', 'boundary_change', 'activity'],
#     'quarantine': ['activity'],
#     'heritage': ['deletion', 'boundary_change'],
#     'contract': ['transition'],
#     'easement': ['transition', 'boundary_change'],
# }


# async def get_active_protection(
#     self, field_id: UUID
# ) -> FieldProtection | None:
#     result = await self.session.execute(
#         select(FieldProtection).where(
#             FieldProtection.field_id == field_id,
#             or_(
#                 FieldProtection.expires_at.is_(None),
#                 FieldProtection.expires_at > datetime.now(timezone.utc),
#             ),
#         )
#     )
#     return result.scalar_one_or_none()

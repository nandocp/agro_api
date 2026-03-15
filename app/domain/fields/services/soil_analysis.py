# # ========== Calculated chemical values ==========
# sum_of_bases_mmol_dm3: Mapped[Decimal | None] = mapped_column(
#     Numeric(7, 2),
#     Computed(
#         '''CASE WHEN calcium_mmol_dm3 IS NOT NULL
#                 AND magnesium_mmol_dm3 IS NOT NULL
#                 AND potassium_mmol_dm3 IS NOT NULL
#            THEN calcium_mmol_dm3 + magnesium_mmol_dm3 + potassium_mmol_dm3
#            ELSE NULL END''',
#         persisted=True,
#     ),
#     init=False,
#     comment='SB = Ca + Mg + K',
# )
# cation_exchange_capacity_mmol_dm3: Mapped[Decimal | None] = mapped_column(
#     Numeric(7, 2),
#     Computed(
#         '''CASE WHEN calcium_mmol_dm3 IS NOT NULL
#                 AND magnesium_mmol_dm3 IS NOT NULL
#                 AND potassium_mmol_dm3 IS NOT NULL
#                 AND hydrogen_aluminum_mmol_dm3 IS NOT NULL
#            THEN calcium_mmol_dm3 + magnesium_mmol_dm3
#                 + potassium_mmol_dm3 + hydrogen_aluminum_mmol_dm3
#            ELSE NULL END''',
#         persisted=True,
#     ),
#     init=False,
#     comment='CTC = SB + H+Al',
# )
# base_saturation_percent: Mapped[Decimal | None] = mapped_column(
#     Numeric(5, 2),
#     Computed(
#         '''CASE WHEN calcium_mmol_dm3 IS NOT NULL
#                 AND magnesium_mmol_dm3 IS NOT NULL
#                 AND potassium_mmol_dm3 IS NOT NULL
#                 AND hydrogen_aluminum_mmol_dm3 IS NOT NULL
#                 AND (calcium_mmol_dm3 + magnesium_mmol_dm3
#                     + potassium_mmol_dm3
#                     + hydrogen_aluminum_mmol_dm3) > 0
#            THEN ROUND(
#                (calcium_mmol_dm3 + magnesium_mmol_dm3 + potassium_mmol_dm3)
#                / (calcium_mmol_dm3 + magnesium_mmol_dm3
#                   + potassium_mmol_dm3 + hydrogen_aluminum_mmol_dm3)
#                * 100, 2)
#            ELSE NULL END''',
#         persisted=True,
#     ),
#     init=False,
#     comment='V% = SB/CTC * 100',
# )
# aluminum_saturation_percent: Mapped[Decimal | None] = mapped_column(
#     Numeric(5, 2),
#     Computed(
#         '''CASE WHEN aluminum_mmol_dm3 IS NOT NULL
#                 AND calcium_mmol_dm3 IS NOT NULL
#                 AND magnesium_mmol_dm3 IS NOT NULL
#                 AND potassium_mmol_dm3 IS NOT NULL
#                 AND (aluminum_mmol_dm3 + calcium_mmol_dm3
#                     + magnesium_mmol_dm3 + potassium_mmol_dm3) > 0
#            THEN ROUND(
#                aluminum_mmol_dm3
#                / (aluminum_mmol_dm3 + calcium_mmol_dm3
#                   + magnesium_mmol_dm3 + potassium_mmol_dm3)
#                * 100, 2)
#            ELSE NULL END''',
#         persisted=True,
#     ),
#     init=False,
#     comment='m% = Al/(SB+Al) * 100',
# )

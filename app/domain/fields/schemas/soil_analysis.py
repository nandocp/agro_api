# class SoilAnalysisCreate(BaseModel):
#     organic_matter_percent: Decimal | None = Field(None, ge=0, le=100)
#     base_saturation_percent: Decimal | None = Field(None, ge=0, le=100)
#     clay_percent: Decimal | None = Field(None, ge=0, le=100)
#     silt_percent: Decimal | None = Field(None, ge=0, le=100)
#     sand_percent: Decimal | None = Field(None, ge=0, le=100)
#     field_capacity_percent: Decimal | None = Field(None, ge=0, le=100)
#     wilting_point_percent: Mapped | None = Field(None, ge=0, le=100)

#     @model_validator(mode='after')
#     def validate_texture_sum(self) -> 'SoilAnalysisCreate':
#         values = [self.clay_percent, self.silt_percent, self.sand_percent]
#         if all(v is not None for v in values):
#             total = sum(values)
#             if not (99 <= total <= 101):
#                 raise ValueError('Clay + silt + sand must sum to 100%')
#         return self

# class SoilAnalysisResponse(BaseSchema):
#     # ...
#     organic_matter_g_dm3: Decimal | None

#     @computed_field
#     @property
#     def organic_matter_percent(self) -> Decimal | None:
#         if self.organic_matter_g_dm3 is None:
#             return None
#         return round(self.organic_matter_g_dm3 / 10, 2)

# # app/domain/fields/schemas/soil_analysis.py
# class ChemicalData(BaseModel):
#     ph_water: Decimal | None = Field(None, ge=0, le=14)
#     ph_cacl2: Decimal | None = Field(None, ge=0, le=14)
#     organic_matter_g_dm3: Decimal | None = Field(None, ge=0)
#     phosphorus_mg_dm3: Decimal | None = Field(None, ge=0)
#     potassium_mmol_dm3: Decimal | None = Field(None, ge=0)
#     calcium_mmol_dm3: Decimal | None = Field(None, ge=0)
#     magnesium_mmol_dm3: Decimal | None = Field(None, ge=0)
#     aluminum_mmol_dm3: Decimal | None = Field(None, ge=0)
#     hydrogen_aluminum_mmol_dm3: Decimal | None = Field(None, ge=0)
#     sulfur_mg_dm3: Decimal | None = Field(None, ge=0)
#     boron_mg_dm3: Decimal | None = Field(None, ge=0)
#     copper_mg_dm3: Decimal | None = Field(None, ge=0)
#     iron_mg_dm3: Decimal | None = Field(None, ge=0)
#     manganese_mg_dm3: Decimal | None = Field(None, ge=0)
#     zinc_mg_dm3: Decimal | None = Field(None, ge=0)


# class PhysicalData(BaseModel):
#     clay_percent: Decimal | None = Field(None, ge=0, le=100)
#     silt_percent: Decimal | None = Field(None, ge=0, le=100)
#     total_sand_percent: Decimal | None = Field(None, ge=0, le=100)
#     fine_sand_percent: Decimal | None = Field(None, ge=0, le=100)
#     coarse_sand_percent: Decimal | None = Field(None, ge=0, le=100)
#     texture_class: str | None = None
#     bulk_density_g_cm3: Decimal | None = Field(None, ge=0)
#     particle_density_g_cm3: Decimal | None = Field(None, ge=0)
#     total_porosity_percent: Decimal | None = Field(None, ge=0, le=100)
#     field_capacity_percent: Decimal | None = Field(None, ge=0, le=100)
#     wilting_point_percent: Decimal | None = Field(None, ge=0, le=100)
#     available_water_mm: Decimal | None = Field(None, ge=0)

#     @model_validator(mode='after')
#     def validate_texture_sum(self) -> 'PhysicalData':
#         values = [
#             self.clay_percent,
#             self.silt_percent,
#             self.total_sand_percent,
#         ]
#         if all(v is not None for v in values):
#             if not (99 <= sum(values) <= 101):
#                 raise ValueError('Clay + silt + sand must sum to 100%')
#         return self


# class BiologicalData(BaseModel):
#     microbial_biomass_carbon_mg_kg: Decimal | None = Field(None, ge=0)
#     basal_respiration_mg_co2_kg_day: Decimal | None = Field(None, ge=0)
#     metabolic_quotient: Decimal | None = Field(None, ge=0)
#     total_nitrogen_g_kg: Decimal | None = Field(None, ge=0)
#     ammonium_nitrogen_mg_kg: Decimal | None = Field(None, ge=0)
#     nitrate_nitrogen_mg_kg: Decimal | None = Field(None, ge=0)


# class SoilAnalysisCreate(BaseModel):
#     field_id: UUID
#     collected_at: date
#     analyzed_at: date | None = None
#     sampling_depth_cm: int = Field(gt=0)
#     protocol: str | None = None
#     chemical: ChemicalData | None = None
#     physical: PhysicalData | None = None
#     biological: BiologicalData | None = None
#     collector_name: str
#     collector_registry: str
#     laboratory: str

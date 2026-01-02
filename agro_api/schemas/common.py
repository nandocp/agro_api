from pydantic import BaseModel, Field


class FilterPage():
    offset: int = Field(ge=0, default=0)
    limit: int = Field(ge=0, default=10)

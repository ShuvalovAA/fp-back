from typing import TypeAlias

from django.http import HttpResponse
from django.utils.html import escape
from drf_spectacular.utils import OpenApiParameter
from pydantic import BaseModel, Field, field_serializer, field_validator

from .models import Income

IncomeId: TypeAlias = int


DeletedIncomeIdParametr = OpenApiParameter(
    name='IncomeId',
    type=IncomeId,
    description='Object ID to delete',
    required=True,
)


class ToDeleteIncomeId(BaseModel):
    value: IncomeId = Field(ge=1)

    @field_validator('value')
    @classmethod
    def parse_value(cls, v: list[str]):
        if len(v) != 1:
            raise ValueError
        value: str = v[0]
        return IncomeId(value)


class DeletedIncomeResponse(BaseModel):
    id: int = Field(ge=1)
    is_deleted: bool = Field(default=True)
    name: str = Field(min_length=1)

    @field_serializer('name')
    @classmethod
    def escape_name(cls, v: str) -> str:
        return escape(v)


def delete_income(to_delete_income_id: IncomeId) -> HttpResponse:

    income = Income.objects.get(pk=to_delete_income_id, is_deleted=False)
    income.is_deleted = True
    income.save()

    content = DeletedIncomeResponse(
        id=income.id,
        is_deleted=income.is_deleted,
        name=income.name
    ).model_dump_json()
    return HttpResponse(status=201, content=content)

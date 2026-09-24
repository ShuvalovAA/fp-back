from datetime import date
from decimal import Decimal

from django.http import HttpResponse
from django.utils.html import escape
from pydantic import BaseModel, Field, field_serializer, field_validator

from ..utils.time_utils.now import get_now
from .models import Income, IncomeState


class NewIncome(BaseModel):
    name: str = Field(min_length=1)
    state: IncomeState = Field()
    received_date: date = Field()
    amount: Decimal = Field(gt=0, le=Decimal(100000000000000))
    is_deleted: bool = Field(default=False)

    @field_validator('received_date')
    @classmethod
    def validate_received_date(cls, v: date) -> date:
        if v.year < 2000:
            raise ValueError('Дата не может быть раньше 2000 года')
        return v

    @field_serializer('name')
    @classmethod
    def escape_name(cls, v: str) -> str:
        return escape(v)


class NewIncomeResponse(BaseModel):
    id: int = Field(ge=1)
    name: str = Field(min_length=1)
    state: IncomeState = Field()
    received_date: date = Field()
    amount: Decimal = Field(gt=0, le=Decimal(100000000000000))
    is_deleted: bool = Field(default=False)


def add_income(new_income: NewIncome) -> HttpResponse:
    def __prepare_content(new_income: NewIncome, id: int) -> str:
        content = new_income.model_dump()
        content.update({'id': id})
        return NewIncomeResponse(**content).model_dump_json()
    now = get_now()
    id = Income.objects.create(
        name=new_income.name,
        state=new_income.state,
        create_date=now,
        update_date=now,
        received_date=new_income.received_date,
        received_month=new_income.received_date.month,
        received_month_day=new_income.received_date.day,
        amount=new_income.amount,
        is_deleted=new_income.is_deleted,
    ).id
    content = __prepare_content(new_income, id)
    return HttpResponse(status=201, content=content)

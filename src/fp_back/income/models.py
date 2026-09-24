from datetime import date, datetime
from decimal import Decimal
from typing import Any, cast

from django.db.models import (
    BigAutoField,
    BooleanField,
    DateField,
    DateTimeField,
    DecimalField,
    IntegerChoices,
    Model,
    PositiveSmallIntegerField,
    TextField,
)

from .manager import IncomeManager


class IncomeState(IntegerChoices):
    EXECUTED = 1, 'EXECUTED'
    NOT_EXECUTED = 2, 'NOT_EXECUTED'


class Income(Model):
    id = cast(int, BigAutoField(primary_key=True))
    name = cast(str, TextField(null=False))
    state = cast(int, PositiveSmallIntegerField(
        null=False,
        choices=IncomeState.choices,
        default=IncomeState.NOT_EXECUTED
    ))
    create_date = cast(datetime, DateTimeField(null=False))
    update_date = cast(datetime, DateTimeField(null=False))
    received_date = cast(date, DateField(null=False))
    amount = cast(Decimal, DecimalField(null=False, max_digits=999999999, decimal_places=2))
    received_month = cast(int, PositiveSmallIntegerField(null=False))
    received_month_day = cast(int, PositiveSmallIntegerField(null=False))
    is_deleted = cast(bool, BooleanField(default=False, null=False))

    def save(self, *args: Any, **kwargs: Any):
        self.full_clean()
        super().save(*args, **kwargs)

    objects = IncomeManager()

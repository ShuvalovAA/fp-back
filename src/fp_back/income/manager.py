from __future__ import annotations

from typing import TYPE_CHECKING

from django.db.models import Manager, QuerySet

if TYPE_CHECKING:
    from .models import Income


class IncomeManager(Manager['Income']):

    def get_only_no_deleted(self) -> QuerySet[Income]:
        return self.filter(is_deleted=False)

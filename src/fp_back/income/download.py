from typing import Any

from django.http import HttpResponse


# TODO: заменить Any на конкретный тип
def download_income(request: Any) -> HttpResponse:
    return HttpResponse(200)

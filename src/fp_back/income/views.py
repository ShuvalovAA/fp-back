from django.db.models import ObjectDoesNotExist
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
)
from django.http.request import QueryDict
from drf_spectacular.utils import extend_schema
from pydantic import ValidationError
from rest_framework.decorators import api_view
from rest_framework.request import Request

from fp_back.typing.http.methods import AllowedMethods

from .add import NewIncome, NewIncomeResponse, add_income

# from .copy import copy_income
from .delete import (
    DeletedIncomeIdParametr,
    DeletedIncomeResponse,
    ToDeleteIncomeId,
    IncomeId,
    delete_income,
)

# from .download import download_income
# from .edit import edit_income
# from .upload import upload_income


@extend_schema(
    request=NewIncome,
    responses={
        201: NewIncomeResponse,
        400: {'description': 'Bad Request'},
    },
)
@api_view([AllowedMethods.POST])
def add(request: Request) -> HttpResponse | HttpResponseBadRequest:
    try:
        new_income = NewIncome(
            **request.data
        )
        return add_income(new_income=new_income)
    except ValidationError as error:
        return HttpResponseBadRequest(error)


@extend_schema(
    parameters=[
        DeletedIncomeIdParametr
    ],
    responses={
        200: DeletedIncomeResponse,
        400: {'description': 'Bad Request'},
        404: {'description': 'Not Found'},
    },
)
@api_view([AllowedMethods.DELETE])
def delete(request: Request) -> HttpResponse | HttpResponseBadRequest | HttpResponseNotFound:
    query_params: QueryDict = request.query_params
    to_delete_income_id = ToDeleteIncomeId(**query_params).value    #  TODO: this any shiet, must remake
    try:
        return delete_income(to_delete_income_id=to_delete_income_id)
    except ValidationError as error:
        return HttpResponseBadRequest(error)
    except ObjectDoesNotExist as error:
        return HttpResponseNotFound(error)

# def copy(request: HttpRequest) -> HttpResponse:
#     return copy_income(request=request)

# def edit(request: HttpRequest) -> HttpResponse:
#     return edit_income(request=request)

# def upload(request: HttpRequest) -> HttpResponse:
#     return upload_income(request=request)


# def download(request: HttpRequest) -> HttpResponse:
#     return download_income(request=request)

from enum import Enum


class AllowedMethods(str, Enum):
    POST = 'POST'
    GET = 'GET'
    DELETE = 'DELETE'
    PUT = 'PUT'

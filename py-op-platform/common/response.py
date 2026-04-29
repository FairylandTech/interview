# coding: UTF-8
"""
@software: PyCharm
@author: Beau Dean
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@datetime: 2026-04-29 20:37:45 UTC+08:00
"""
from __future__ import annotations

import typing as t

from django.http import HttpResponse, JsonResponse


class HTTPAPIResponse:

    def __init__(self, code: int, message: str, data: t.Any):
        self.__code = code
        self.__message = message
        self.__data = data

    def __as_dict(self):
        return {"code": self.__code, "message": self.__message, "data": self.__data}

    @property
    def as_response(self) -> HttpResponse:
        return JsonResponse(self.__as_dict(), status=self.__code)

    @classmethod
    def build(cls, code: int = None, message: str = None, data: t.Any = None):
        if code is None:
            code = 200

        if message is None:
            message = "ok"

        if data is None:
            data = {}

        return cls(code, message, data)

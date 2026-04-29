# coding: UTF-8
"""
@software: PyCharm
@author: Beau Dean
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@datetime: 2026-04-29 23:09:27 UTC+08:00
"""
from __future__ import annotations

import logging
import time
import typing as t


class TTFBMiddleware:
    """
    每个请求耗时

    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)

    def __call__(self, request):
        start = time.time()

        response = self.get_response(request)

        duration = time.time() - start

        self.logger.info(f">>> method={request.method} path={request.path} duration={duration:.2f}")

        return response

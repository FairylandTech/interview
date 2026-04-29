# coding: UTF-8
"""
@software: PyCharm
@author: Beau Dean
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@datetime: 2026-04-29 19:17:48 UTC+08:00
"""
from __future__ import annotations

import os
import typing as t

import orjson
from django.conf import settings

from domain.model.config import Config


class ConfigUtils:
    __loaded__ = False
    __context__: t.ClassVar[Config]

    @classmethod
    def __load(cls):
        if not cls.__loaded__:
            try:
                with open(os.path.join(settings.BASE_DIR, "config.json"), "r") as file:
                    context = orjson.loads(file.read())
                cls.__context__ = Config(**context)
                cls.__loaded__ = True
            except Exception as error:
                raise RuntimeError(f"配置文件载入失败。{error}")

    @classmethod
    def get_config(cls) -> Config:
        cls.__load()
        return cls.__context__

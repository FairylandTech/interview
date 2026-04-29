# coding: UTF-8
"""
@software: PyCharm
@author: Beau Dean
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@datetime: 2026-04-29 18:55:35 UTC+08:00
"""
from __future__ import annotations

import typing as t

from django.db import models


class EnabledChoices(models.TextChoices):
    YES = "Y", "是"
    NO = "N", "否"

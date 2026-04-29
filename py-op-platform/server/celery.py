# coding: UTF-8
"""
@software: PyCharm
@author: Beau Dean
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@datetime: 2026-04-30 01:05:32 UTC+08:00
"""
from __future__ import annotations

import os
import typing as t

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

celery_app = Celery("server")
celery_app.config_from_object("django.conf:settings", namespace="server-celery")
celery_app.autodiscover_tasks()

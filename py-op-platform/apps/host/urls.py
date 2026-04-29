# coding: UTF-8
"""
@software: PyCharm
@author: Beau Dean
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@datetime: 2026-04-29 22:56:13 UTC+08:00
"""
from __future__ import annotations

import typing as t

from django.urls import path, URLPattern
from apps.host.views import HostMachineView
from apps.host.views import HostMachinePasswordView
from apps.host.views import HostMachinePingView
from apps.host.views import HostRoomView
from apps.host.views import HostRegionView

urlpatterns: list[URLPattern] = [
    path("", HostMachineView.as_view(), name="host"),
    path("<int:machine_id>/password/", HostMachinePasswordView.as_view(), name="host-password"),
    path("<str:host>/ping/", HostMachinePingView.as_view(), name="host-ping"),
    path("room/", HostRoomView.as_view(), name="room"),
    path("region/", HostRegionView.as_view(), name="region"),
]

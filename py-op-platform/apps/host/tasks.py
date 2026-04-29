# coding: UTF-8
"""
@software: PyCharm
@author: Beau Dean
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@datetime: 2026-04-30 01:24:30 UTC+08:00
"""
from __future__ import annotations

import typing as t

import secrets
import string

from celery import shared_task
from django.db import transaction
from django.db.models import Count
from django.utils import timezone

from common.field import EnabledChoices
from apps.host.models import (
    HostMachineModel,
    HostRegionModel,
    HostRegionStatisticHostModel,
    HostRoomModel,
    HostRoomStatisticHostModel,
)
from utils.config import ConfigUtils
from utils.password import PasswordUtils

__SECRET_KEY = ConfigUtils.get_config().secret_key


@shared_task
def rotate_host_passwords():
    now = timezone.now()

    machines = list(HostMachineModel.objects.filter(enabled=EnabledChoices.YES))

    for machine in machines:
        machine.password = PasswordUtils.encrypt_password(PasswordUtils.generate_password(), __SECRET_KEY)
        machine.updated_at = now

    if machines:
        HostMachineModel.objects.bulk_update(machines, ["password", "updated_at"])

    return {
        "updated": len(machines),
    }


@shared_task
def statistic_host_count():
    now = timezone.now()

    with transaction.atomic():
        # 把历史的数据状态全部修改为N
        HostRoomStatisticHostModel.objects.filter(
            enabled=EnabledChoices.YES,
        ).update(
            enabled=EnabledChoices.NO,
            updated_at=now,
        )

        HostRegionStatisticHostModel.objects.filter(
            enabled=EnabledChoices.YES,
        ).update(
            enabled=EnabledChoices.NO,
            updated_at=now,
        )

        # 区域维度统计机房数量
        region_statistics = HostRegionModel.objects.filter(
            enabled=EnabledChoices.YES,
            region_rooms__enabled=EnabledChoices.YES,
            region_rooms__room__enabled=EnabledChoices.YES,
            region_rooms__room__room_machines__enabled=EnabledChoices.YES,
            region_rooms__room__room_machines__machine__enabled=EnabledChoices.YES,
        ).annotate(total=Count("region_rooms__room__room_machines__machine", distinct=True))

        HostRegionStatisticHostModel.objects.bulk_create(
            [
                HostRegionStatisticHostModel(
                    region=region,
                    total=region.total,
                    created_at=now,
                    updated_at=now,
                    enabled=EnabledChoices.YES,
                )
                for region in region_statistics
            ]
        )

        # 机房维度统计主机数量
        room_statistics = HostRoomModel.objects.filter(
            enabled=EnabledChoices.YES,
            room_machines__enabled=EnabledChoices.YES,
            room_machines__machine__enabled=EnabledChoices.YES,
        ).annotate(total=Count("room_machines__machine", distinct=True))

        HostRoomStatisticHostModel.objects.bulk_create(
            [
                HostRoomStatisticHostModel(
                    room=room,
                    total=room.total,
                    created_at=now,
                    updated_at=now,
                    enabled=EnabledChoices.YES,
                )
                for room in room_statistics
            ]
        )

    return {
        "room_statistics": len(room_statistics),
        "region_statistics": len(region_statistics),
    }

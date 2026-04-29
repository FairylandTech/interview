# coding: UTF-8
"""
@software: PyCharm
@author: Beau Dean
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@datetime: 2026-04-30 00:19:54 UTC+08:00
"""
from __future__ import annotations

import typing as t

import ipaddress

from apps.host.models import HostMachineModel, HostRegionModel, HostRoomModel


class HostMachineSerializer:

    @classmethod
    def serialize(cls, machine: HostMachineModel) -> dict[str, t.Any]:
        return {
            "id": machine.id,
            "hostName": machine.hostname,
            "ipv4": str(ipaddress.ip_address(machine.ipv4)),
            "online": machine.online,
            "createdAt": machine.created_at.strftime("%Y-%m-%d %H:%M:%S") if machine.created_at else None,
            "updatedAt": machine.updated_at.strftime("%Y-%m-%d %H:%M:%S") if machine.updated_at else None,
            "enabled": machine.enabled,
        }

    @classmethod
    def serialize_many(cls, machines: t.Iterable[HostMachineModel]) -> list[dict[str, t.Any]]:
        return [cls.serialize(machine) for machine in machines]


class HostRoomSerializer:

    @classmethod
    def serialize(cls, room: HostRoomModel) -> dict[str, t.Any]:
        return {
            "id": room.id,
            "name": room.name,
            "createdAt": room.created_at.strftime("%Y-%m-%d %H:%M:%S") if room.created_at else None,
            "updatedAt": room.updated_at.strftime("%Y-%m-%d %H:%M:%S") if room.updated_at else None,
            "enabled": room.enabled,
        }

    @classmethod
    def serialize_many(cls, rooms: t.Iterable[HostRoomModel]) -> list[dict[str, t.Any]]:
        return [cls.serialize(room) for room in rooms]


class HostRegionSerializer:

    @classmethod
    def serialize(cls, region: HostRegionModel) -> dict[str, t.Any]:
        return {
            "id": region.id,
            "name": region.name,
            "createdAt": region.created_at.strftime("%Y-%m-%d %H:%M:%S") if region.created_at else None,
            "updatedAt": region.updated_at.strftime("%Y-%m-%d %H:%M:%S") if region.updated_at else None,
            "enabled": region.enabled,
        }

    @classmethod
    def serialize_many(cls, regions: t.Iterable[HostRegionModel]) -> list[dict[str, t.Any]]:
        return [cls.serialize(region) for region in regions]

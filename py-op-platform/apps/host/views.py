import logging

import orjson
from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from django.views import View

from apps.host.models import (
    HostMachineModel,
    HostRegionModel,
    HostRegionRoomModel,
    HostRoomMachineModel,
    HostRoomModel,
)
from apps.host.serializer import HostMachineSerializer, HostRegionSerializer, HostRoomSerializer
from common.response import HTTPAPIResponse
from utils.config import ConfigUtils
from utils.password import PasswordUtils

# Create your views here.

logger = logging.getLogger(__name__)


class HostMachineView(View):

    __SECRET_KEY = ConfigUtils.get_config().secret_key

    def get(self, request: HttpRequest) -> HttpResponse:
        hostname: str = request.GET.get("hostName", "")
        room_id: str = request.GET.get("roomId", "")
        region_id: str = request.GET.get("regionId", "")
        page: str = request.GET.get("page", "1")
        size: str = request.GET.get("size", "10")

        hosts: QuerySet[HostMachineModel] = HostMachineModel.objects.filter(enabled="Y")

        if hostname:
            hosts = hosts.filter(hostname__icontains=hostname)

        if room_id:
            hosts = hosts.filter(
                room_machines__room_id=room_id,
                room_machines__enabled="Y",
            )

        if region_id:
            hosts = hosts.filter(
                room_machines__room__region_rooms__region_id=region_id,
                room_machines__room__region_rooms__enabled="Y",
                room_machines__enabled="Y",
            )

        hosts = hosts.distinct().order_by("-id")
        paginator = Paginator(hosts, size)
        dataset = paginator.get_page(page)

        return HTTPAPIResponse.build(
            data={
                "total": paginator.count,
                "page": dataset.number,
                "size": int(size),
                "items": HostMachineSerializer.serialize_many(dataset.object_list),
            }
        ).as_response

    def post(self, request: HttpRequest) -> HttpResponse:
        try:
            body: dict[str, str] = orjson.loads(request.body.decode("UTF-8") or "{}")
        except Exception as error:
            logger.error(f"Error: {error}")
            return HTTPAPIResponse.build(code=400, message="请求体不合法").as_response

        hostname: str = body.get("hostName", "")
        ipv4: int = int(body.get("ipv4", 0))
        online: str = body.get("online", HostMachineModel.OnlineChoices.NO)
        room_id: int = int(body.get("roomId", 0))

        if not hostname:
            return HTTPAPIResponse.build(code=400, message="主机名称不能为空").as_response

        if not ipv4:
            return HTTPAPIResponse.build(code=400, message="主机IPv4不能为空").as_response

        if not room_id:
            return HTTPAPIResponse.build(code=400, message="机房ID不能为空").as_response

        room = HostRoomModel.objects.get(id=room_id, enabled="Y")
        now = timezone.now()
        machine = HostMachineModel.objects.create(
            hostname=hostname,
            password=PasswordUtils.encrypt_password(PasswordUtils.generate_password(), self.__SECRET_KEY),
            ipv4=ipv4,
            online=online,
            created_at=now,
            updated_at=now,
        )
        HostRoomMachineModel.objects.create(
            room=room,
            machine=machine,
            created_at=now,
            updated_at=now,
        )

        return HTTPAPIResponse.build(data=HostMachineSerializer.serialize(machine)).as_response

    def put(self, request: HttpRequest) -> HttpResponse:
        try:
            body: dict[str, str] = orjson.loads(request.body.decode("UTF-8") or "{}")
        except Exception as error:
            logger.error(f"Error: {error}")
            return HTTPAPIResponse.build(code=400, message="请求体不合法").as_response

        machine_id: int = int(body.get("id", "0"))
        hostname: str = body.get("hostName", "")
        ipv4: int = int(body.get("ipv4", 0))
        online: str = body.get("online", "")
        room_id: int = int(body.get("roomId", 0))

        if not machine_id:
            return HTTPAPIResponse.build(code=400, message="主机ID不能为空").as_response

        machine = HostMachineModel.objects.get(id=machine_id, enabled="Y")
        update_fields = ["updated_at"]

        if hostname:
            machine.hostname = hostname
            update_fields.append("hostname")

        if ipv4:
            machine.ipv4 = ipv4
            update_fields.append("ipv4")

        if online:
            machine.online = online
            update_fields.append("online")

        machine.updated_at = timezone.now()
        machine.save(update_fields=update_fields)

        if room_id:
            now = timezone.now()
            HostRoomMachineModel.objects.filter(machine=machine, enabled="Y").update(enabled="N", updated_at=now)
            room = HostRoomModel.objects.get(id=room_id, enabled="Y")
            HostRoomMachineModel.objects.create(
                room=room,
                machine=machine,
                created_at=now,
                updated_at=now,
            )

        return HTTPAPIResponse.build(data=HostMachineSerializer.serialize(machine)).as_response

    def delete(self, request: HttpRequest) -> HttpResponse:
        machine_id: str = request.GET.get("id", "")

        if not machine_id:
            return HTTPAPIResponse.build(code=400, message="主机ID不可以为空").as_response

        now = timezone.now()
        machine = HostMachineModel.objects.get(id=machine_id)
        machine.enabled = "N"
        machine.updated_at = now
        machine.save(update_fields=["updated_at", "enabled"])
        HostRoomMachineModel.objects.filter(machine=machine, enabled="Y").update(enabled="N", updated_at=now)

        return HTTPAPIResponse.build().as_response


class HostRoomView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        room_name: str = request.GET.get("name", "")
        region_id: str = request.GET.get("regionId", "")
        page: str = request.GET.get("page", "1")
        size: str = request.GET.get("size", "10")

        rooms: QuerySet[HostRoomModel] = HostRoomModel.objects.filter(enabled="Y")

        if room_name:
            rooms = rooms.filter(name__icontains=room_name)

        if region_id:
            rooms = rooms.filter(
                region_rooms__region_id=region_id,
                region_rooms__enabled="Y",
            )

        rooms = rooms.distinct().order_by("-id")
        paginator = Paginator(rooms, size)
        dataset = paginator.get_page(page)

        return HTTPAPIResponse.build(
            data={
                "total": paginator.count,
                "page": dataset.number,
                "size": int(size),
                "items": HostRoomSerializer.serialize_many(dataset.object_list),
            }
        ).as_response

    def post(self, request: HttpRequest) -> HttpResponse:
        try:
            body: dict[str, str] = orjson.loads(request.body.decode("UTF-8") or "{}")
        except Exception as error:
            logger.error(f"Error: {error}")
            return HTTPAPIResponse.build(code=400, message="请求体不合法").as_response

        name: str = body.get("name", "")
        region_id: int = int(body.get("regionId", 0))

        if not name:
            return HTTPAPIResponse.build(code=400, message="机房名称不能为空").as_response

        if not region_id:
            return HTTPAPIResponse.build(code=400, message="区域ID不能为空").as_response

        region = HostRegionModel.objects.get(id=region_id, enabled="Y")
        now = timezone.now()
        room = HostRoomModel.objects.create(name=name, created_at=now, updated_at=now)
        HostRegionRoomModel.objects.create(
            region=region,
            room=room,
            created_at=now,
            updated_at=now,
        )

        return HTTPAPIResponse.build(data=HostRoomSerializer.serialize(room)).as_response

    def put(self, request: HttpRequest) -> HttpResponse:
        try:
            body: dict[str, str] = orjson.loads(request.body.decode("UTF-8") or "{}")
        except Exception as error:
            logger.error(f"Error: {error}")
            return HTTPAPIResponse.build(code=400, message="请求体不合法").as_response

        room_id: int = int(body.get("id", "0"))
        name: str = body.get("name", "")
        region_id: int = int(body.get("regionId", 0))

        if not room_id:
            return HTTPAPIResponse.build(code=400, message="机房ID不能为空").as_response

        room = HostRoomModel.objects.get(id=room_id, enabled="Y")

        if name:
            room.name = name
            room.updated_at = timezone.now()
            room.save(update_fields=["name", "updated_at"])

        if region_id:
            now = timezone.now()
            HostRegionRoomModel.objects.filter(room=room, enabled="Y").update(enabled="N", updated_at=now)
            region = HostRegionModel.objects.get(id=region_id, enabled="Y")
            HostRegionRoomModel.objects.create(
                region=region,
                room=room,
                created_at=now,
                updated_at=now,
            )

        return HTTPAPIResponse.build(data=HostRoomSerializer.serialize(room)).as_response

    def delete(self, request: HttpRequest) -> HttpResponse:
        room_id: str = request.GET.get("id", "")

        if not room_id:
            return HTTPAPIResponse.build(code=400, message="机房ID不可以为空").as_response

        now = timezone.now()
        room = HostRoomModel.objects.get(id=room_id)
        room.enabled = "N"
        room.updated_at = now
        room.save(update_fields=["updated_at", "enabled"])
        HostRegionRoomModel.objects.filter(room=room, enabled="Y").update(enabled="N", updated_at=now)
        HostRoomMachineModel.objects.filter(room=room, enabled="Y").update(enabled="N", updated_at=now)

        return HTTPAPIResponse.build().as_response


class HostRegionView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        region_name: str = request.GET.get("name", "")
        page: str = request.GET.get("page", "1")
        size: str = request.GET.get("size", "10")

        regions: QuerySet[HostRegionModel] = HostRegionModel.objects.filter(enabled="Y")

        if region_name:
            regions = regions.filter(name__icontains=region_name)

        regions = regions.distinct().order_by("-id")
        paginator = Paginator(regions, size)
        dataset = paginator.get_page(page)

        return HTTPAPIResponse.build(
            data={
                "total": paginator.count,
                "page": dataset.number,
                "size": int(size),
                "items": HostRegionSerializer.serialize_many(dataset.object_list),
            }
        ).as_response

    def post(self, request: HttpRequest) -> HttpResponse:
        try:
            body: dict[str, str] = orjson.loads(request.body.decode("UTF-8") or "{}")
        except Exception as error:
            logger.error(f"Error: {error}")
            return HTTPAPIResponse.build(code=400, message="请求体不合法").as_response

        name = body.get("name", "")

        if not name:
            return HTTPAPIResponse.build(code=400, message="区域名称不能为空").as_response

        now = timezone.now()
        region = HostRegionModel.objects.create(name=name, created_at=now, updated_at=now)

        return HTTPAPIResponse.build(data=HostRegionSerializer.serialize(region)).as_response

    def put(self, request: HttpRequest) -> HttpResponse:
        try:
            body: dict[str, str] = orjson.loads(request.body.decode("UTF-8") or "{}")
        except Exception as error:
            logger.error(f"Error: {error}")
            return HTTPAPIResponse.build(code=400, message="请求体不合法").as_response

        region_id: int = int(body.get("id", "0"))
        name: str = body.get("name", "")

        if (not region_id and region_id != 0) and not name:
            return HTTPAPIResponse.build(code=400, message="区域ID或区域名称不可为空")

        region = HostRegionModel.objects.get(id=region_id, enabled="Y")
        region.name = name
        region.updated_at = timezone.now()
        region.save(update_fields=["name", "updated_at"])

        return HTTPAPIResponse.build(data=HostRegionSerializer.serialize(region)).as_response

    def delete(self, request: HttpRequest) -> HttpResponse:
        region_id: str = request.GET.get("id", "")

        if not region_id:
            return HTTPAPIResponse.build(code=400, message="区域ID不可以为空")

        region = HostRegionModel.objects.get(id=region_id)
        region.enabled = "N"
        region.updated_at = timezone.now()
        region.save(update_fields=["updated_at", "enabled"])

        return HTTPAPIResponse.build().as_response


class HostMachinePasswordView(View):

    __SECRET_KEY = ConfigUtils.get_config().secret_key

    def get(self, request: HttpRequest, machine_id: int) -> HttpResponse:
        try:
            machine = HostMachineModel.objects.get(id=machine_id, enabled="Y")
        except HostMachineModel.DoesNotExist:
            return HTTPAPIResponse.build(code=404, message="主机不存在").as_response

        try:
            password = PasswordUtils.decrypt_password(machine.password, self.__SECRET_KEY)
        except Exception as error:
            logger.error(f"Error: {error}")
            return HTTPAPIResponse.build(code=500, message="主机密码解密失败").as_response

        return HTTPAPIResponse.build(
            data={
                "id": machine.id,
                "password": password,
            }
        ).as_response

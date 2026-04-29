from django.db import models

from common.field import EnabledChoices


# Create your models here.


class HostMachineModel(models.Model):
    class OnlineChoices(models.TextChoices):
        YES = "Y", "在线"
        NO = "N", "离线"

    id = models.BigAutoField(primary_key=True, db_comment="主机id")
    hostname = models.CharField(max_length=63, db_comment="主机名称")
    password = models.CharField(max_length=255, db_comment="主机密码")
    ipv4 = models.PositiveIntegerField(db_comment="主机ipv4地址")
    online = models.CharField(max_length=1, choices=OnlineChoices, db_comment="是否在线")
    created_at = models.DateTimeField(db_comment="创建时间")
    updated_at = models.DateTimeField(db_comment="更新时间")
    enabled = models.CharField(max_length=1, choices=EnabledChoices, default=EnabledChoices.YES, db_comment="逻辑状态")

    class Meta:
        db_table = "app_host_machine"
        verbose_name = "主机表"
        verbose_name_plural = "主机表"
        managed = False

    def __str__(self):
        return self.hostname


class HostRoomModel(models.Model):
    id = models.BigAutoField(primary_key=True, db_comment="机房id")
    name = models.CharField(max_length=63, db_comment="机房名称")
    created_at = models.DateTimeField(db_comment="创建时间")
    updated_at = models.DateTimeField(db_comment="更新时间")
    enabled = models.CharField(max_length=1, choices=EnabledChoices, default=EnabledChoices.YES, db_comment="逻辑状态")

    class Meta:
        db_table = "app_host_room"
        verbose_name = "机房表"
        verbose_name_plural = "机房表"
        managed = False

    def __str__(self):
        return self.name


class HostRoomMachineModel(models.Model):
    id = models.BigAutoField(primary_key=True, db_comment="id")
    room = models.ForeignKey(
        HostRoomModel,
        on_delete=models.DO_NOTHING,
        db_column="room_id",
        related_name="room_machines",
        db_comment="机房id",
    )
    machine = models.ForeignKey(
        HostMachineModel,
        on_delete=models.DO_NOTHING,
        db_column="machine_id",
        related_name="room_machines",
        db_comment="机房id",
    )
    created_at = models.DateTimeField(db_comment="创建时间")
    updated_at = models.DateTimeField(db_comment="更新时间")
    enabled = models.CharField(max_length=1, choices=EnabledChoices, default=EnabledChoices.YES, db_comment="逻辑状态")

    class Meta:
        db_table = "app_host_room_machine"
        verbose_name = "机房和主机关联表"
        verbose_name_plural = "机房和主机关联表"
        managed = False


class HostRegionModel(models.Model):
    id = models.BigAutoField(primary_key=True, db_comment="区域id")
    name = models.CharField(max_length=31, db_comment="区域名称")
    created_at = models.DateTimeField(db_comment="创建时间")
    updated_at = models.DateTimeField(db_comment="更新时间")
    enabled = models.CharField(max_length=1, choices=EnabledChoices, default=EnabledChoices.YES, db_comment="逻辑状态")

    class Meta:
        db_table = "app_host_region"
        verbose_name = "区域表"
        verbose_name_plural = "区域表"
        managed = False

    def __str__(self):
        return self.name


class HostRegionRoomModel(models.Model):
    id = models.BigAutoField(primary_key=True, db_comment="id")
    region = models.ForeignKey(
        HostRegionModel,
        on_delete=models.DO_NOTHING,
        db_column="region_id",
        related_name="region_rooms",
        db_comment="区域id",
    )
    room = models.ForeignKey(
        HostRoomModel,
        on_delete=models.DO_NOTHING,
        db_column="room_id",
        related_name="region_rooms",
        db_comment="机房id",
    )
    created_at = models.DateTimeField(db_comment="创建时间")
    updated_at = models.DateTimeField(db_comment="更新时间")
    enabled = models.CharField(max_length=1, choices=EnabledChoices, default=EnabledChoices.YES, db_comment="逻辑状态")

    class Meta:
        db_table = "app_host_region_room"
        verbose_name = "区域和机房关联表"
        verbose_name_plural = "区域和机房关联表"
        managed = False


class HostRegionStatisticHostModel(models.Model):
    id = models.BigAutoField(primary_key=True, db_comment="id")
    region = models.ForeignKey(
        HostRegionModel,
        on_delete=models.DO_NOTHING,
        db_column="region_id",
        related_name="host_statistics",
        db_comment="区域id",
    )
    total = models.IntegerField(default=0, db_comment="统计的数量")
    created_at = models.DateTimeField(db_comment="创建时间")
    updated_at = models.DateTimeField(db_comment="更新时间")
    enabled = models.CharField(max_length=1, choices=EnabledChoices, default=EnabledChoices.YES, db_comment="逻辑状态")

    class Meta:
        db_table = "app_host_region_statistic_host"
        verbose_name = "区域维度统计主机总数"
        verbose_name_plural = "区域维度统计主机总数"
        managed = False


class HostRoomStatisticHostModel(models.Model):
    id = models.BigAutoField(primary_key=True, db_comment="id")
    room = models.ForeignKey(
        HostRoomModel,
        on_delete=models.DO_NOTHING,
        db_column="room_id",
        related_name="host_statistics",
        db_comment="机房id",
    )
    total = models.IntegerField(default=0, db_comment="统计的数量")
    created_at = models.DateTimeField(db_comment="创建时间")
    updated_at = models.DateTimeField(db_comment="更新时间")
    enabled = models.CharField(max_length=1, choices=EnabledChoices, default=EnabledChoices.YES, db_comment="逻辑状态")

    class Meta:
        db_table = "app_host_room_statistic_host"
        verbose_name = "机房维度统计主机总数"
        verbose_name_plural = "机房维度统计主机总数"
        managed = False

# coding: UTF-8
"""
@software: PyCharm
@author: Beau Dean
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@datetime: 2026-04-29 19:29:37 UTC+08:00
"""
from __future__ import annotations

import typing as t

from pydantic import Field

from domain.model import DomainModelBase


class DatabaseConfig(DomainModelBase):
    host: str = Field("localhost", description="数据库地址")
    port: int = Field(3306, description="数据库端口")
    username: str = Field("admin", description="数据库用户名")
    password: t.Optional[str] = Field(None, description="数据库密码")
    database: t.Optional[str] = Field(None, description="数据库名称")


class RedisConfig(DomainModelBase):
    host: str = Field("localhost", description="Redis 主机地址")
    port: int = Field(6379, description="Redis 主机端口号")
    password: str = Field("", description="Redis 认证密码")
    database: int = Field(0, description="Redis 默认库")

    def get_url(self, database: int = None) -> str:
        if not database:
            database = self.database
        return f"redis://{self.password}@{self.host}:{self.port}/{database}"


class Config(DomainModelBase):
    database: dict[str, DatabaseConfig] = Field(dict(), description="数据库配置")
    redis: RedisConfig = Field(RedisConfig(), description="Redis 配置")
    secret_key: str = Field("", description="生成可逆加密密码的 Secret Key")

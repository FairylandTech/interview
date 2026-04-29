import pymysql

from server.celery import celery_app

pymysql.install_as_MySQLdb()

__all__ = [
    "celery_app",
]

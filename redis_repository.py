import logging
from random import random
from time import time
from typing import Callable

import redis
from django.conf import settings

logger = logging.getLogger(__name__)


class RedisUnavailable(Exception):
    pass


def log_error(func: Callable):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except redis.RedisError as exp:
            logger.error("Could not connect to redis")
            logger.exception(exp)
            raise RedisUnavailable('salam')

    return wrapper


class RedisRepository:
    def __init__(self):
        self.redis_connection_pool = redis.ConnectionPool(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            max_connections=4,
            health_check_interval=30,
            socket_timeout=0.5,
        )
        self.health_check_interval = 10
        self.next_health_check = (
            time() + self.health_check_interval + random() * 4 - 2
        )  # noqa: S311

    @property
    def connection(self):
        if self.health_check_interval > 0 and time() > self.next_health_check:
            self.check_health()
        return redis.Redis(connection_pool=self.redis_connection_pool)

    def check_health(self):
        self.next_health_check = time() + self.health_check_interval
        try:
            con = redis.Redis(connection_pool=self.redis_connection_pool)
            con.set("health_check", self.next_health_check)
        except BaseException:  # noqa: WPS424
            self.redis_connection_pool.disconnect()

    @log_error
    def store(self, key, value, expire_in_seconds=None):
        self.connection.set(key, value, expire_in_seconds)

    @log_error
    def get(self, key, get_as_string=True):
        value = self.connection.get(key)
        if get_as_string and value is not None:
            value = value.decode("utf-8")
        return value

    @log_error
    def delete(self, key):
        self.connection.delete(key)


redis_repository = RedisRepository()

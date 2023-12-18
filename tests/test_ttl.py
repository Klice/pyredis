from unittest.mock import Mock

import pytest

from pyredis.redis_server import RedisServer


@pytest.fixture
def time_provider():
    return Mock()


@pytest.fixture
def server(time_provider):
    return RedisServer(time_provider=time_provider)


def test_set_with_ttl_exat(server, time_provider):
    time_provider.get_time.return_value = 1
    server.run(["SET", "key_ttl", "value", "EXAT", 10])
    assert server.run(["GET", "key_ttl"]) == "value"
    time_provider.get_time.return_value = 100
    assert server.run(["GET", "key_ttl"]) == "value"
    time_provider.get_time.return_value = 10 * 1000
    assert server.run(["GET", "key_ttl"]) is None


def test_set_with_ttl_pxat(server, time_provider):
    time_provider.get_time.return_value = 1
    server.run(["SET", "key_ttl", "value", "PXAT", 10])
    assert server.run(["GET", "key_ttl"]) == "value"
    time_provider.get_time.return_value = 9
    assert server.run(["GET", "key_ttl"]) == "value"
    time_provider.get_time.return_value = 10
    assert server.run(["GET", "key_ttl"]) is None


def test_set_with_ttl_ex(server, time_provider):
    time_provider.get_time.return_value = 1
    server.run(["SET", "key_ttl", "value", "EX", 1])
    assert server.run(["GET", "key_ttl"]) == "value"
    time_provider.get_time.return_value = 100
    assert server.run(["GET", "key_ttl"]) == "value"
    time_provider.get_time.return_value = 1001
    assert server.run(["GET", "key_ttl"]) is None


def test_set_with_ttl_px(server, time_provider):
    time_provider.get_time.return_value = 10
    server.run(["SET", "key_ttl", "value", "PX", 5])
    assert server.run(["GET", "key_ttl"]) == "value"
    time_provider.get_time.return_value = 14
    assert server.run(["GET", "key_ttl"]) == "value"
    time_provider.get_time.return_value = 15
    assert server.run(["GET", "key_ttl"]) is None

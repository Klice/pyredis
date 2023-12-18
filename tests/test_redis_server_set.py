import pytest
from pyredis.redis_server import RedisServer
from pyredis.redis_types import SimpleString


@pytest.fixture
def server():
    return RedisServer()


def test_set_get(server):
    assert server.run(["SET", "Key", "Value"]) == SimpleString("OK")
    assert server.run(["GET", "Key"]) == "Value"


def test_set_get_nx(server):
    assert server.run(["SET", "Key", "Value1"]) == SimpleString("OK")
    assert server.run(["SET", "Key", "Value2", "NX"]) == SimpleString("OK")
    assert server.run(["GET", "Key"]) == "Value1"


def test_set_get_xx(server):
    assert server.run(["SET", "Key_xx", "Value1", "XX"]) == SimpleString("OK")
    assert server.run(["GET", "Key_xx"]) is None


def test_set_with_get(server):
    assert server.run(["SET", "Key", "Value1"]) == SimpleString("OK")
    assert server.run(["SET", "Key", "Value2", "GET"]) == "Value1"


def test_set_with_get_nonexistent(server):
    assert server.run(["SET", "Nonexisten_Key", "Value2", "GET"]) is None

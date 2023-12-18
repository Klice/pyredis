import pytest

from pyredis.redis_server import RedisServer
from pyredis.redis_types import RedisError, SimpleString


@pytest.fixture
def server():
    return RedisServer()


def test_ping(server):
    res = server.run(["PING"])
    assert isinstance(res, SimpleString)
    assert res == SimpleString("PONG")


def test_echo(server):
    assert server.run(["ECHO", "Test World"]) == "Test World"


def test_get_nonexistent(server):
    assert server.run(["GET", "nonexistent"]) is None


def test_unknown_command(server):
    res = server.run(["SOMECOMMAND", "Arg"])
    assert isinstance(res, RedisError)
    assert "SOMECOMMAND Arg" in str(res)


def test_config_return_empty(server):
    assert server.run(["CONFIG", "Key", "Value"]) == SimpleString("")


def test_del_one_key(server):
    assert server.run(["DEL", "key"]) == 0
    server.run(["SET", "key", "value"])
    assert server.run(["DEL", "key"]) == 1
    assert server.run(["GET", "key"]) is None


def test_del_multiple(server):
    server.run(["SET", "key1", "value"])
    server.run(["SET", "key2", "value"])
    assert server.run(["DEL", "key1", "key2", "key3"]) == 2

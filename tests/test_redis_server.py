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

import pytest

from pyredis.redis_server import RedisServer
from pyredis.redis_types import RedisError, SimpleString


def cmd(command: str) -> list[str]:
    return command.split(" ")


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


def test_incr(server):
    server.run(["SET", "key_incr", "1"])
    assert server.run(["INCR", "key_incr"]) == 2
    assert server.run(["INCR", "key_incr"]) == 3
    assert server.run(["INCR", "key_incr"]) == 4
    assert server.run(["GET", "key_incr"]) == "4"


def test_incr_nonexistent(server):
    server.run(["DEL", "key_incr"])
    assert server.run(["INCR", "key_incr"]) == 1


def test_incr_invalid_value(server):
    server.run(["SET", "key_incr", "asdfdsf"])
    assert isinstance(server.run(["INCR", "key_incr"]), RedisError)


def test_decr(server):
    server.run(["SET", "key_incr", "2"])
    assert server.run(["DECR", "key_incr"]) == 1
    assert server.run(["DECR", "key_incr"]) == 0
    assert server.run(["DECR", "key_incr"]) == -1
    assert server.run(["GET", "key_incr"]) == "-1"


def test_decr_nonexistent(server):
    server.run(["DEL", "key_incr"])
    assert server.run(["DECR", "key_incr"]) == -1


def test_decr_invalid_value(server):
    server.run(["SET", "key_incr", "asdfdsf"])
    assert isinstance(server.run(["DECR", "key_incr"]), RedisError)


def test_exists(server):
    server.run(["SET", "key1", "value"])
    server.run(["SET", "key2", "value"])
    assert server.run(["EXISTS", "key1", "key2", "key3"]) == 2


def test_exists_nonexistent(server):
    assert server.run(cmd("EXISTS key_nonexistent")) == 0


def test_lpush_one_noexistent(server):
    assert server.run(cmd('LPUSH mylist1 world1')) == 1
    assert server.run(cmd('LPUSH mylist1 world2')) == 2
    assert server.run(cmd('LPUSH mylist1 world3')) == 3
    assert server.run(cmd('LRANGE mylist1 0 -1')) == ["world3", "world2", "world1"]


def test_lpush_insert_multiple(server):
    assert server.run(cmd('LPUSH mylist2 "world" "world" "world"')) == 3
    assert server.run(cmd('LPUSH mylist2 "world" "world" "world"')) == 6


def test_rpush_one_noexistent(server):
    assert server.run(cmd('RPUSH mylist3 world1')) == 1
    assert server.run(cmd('RPUSH mylist3 world2')) == 2
    assert server.run(cmd('RPUSH mylist3 world3')) == 3
    assert server.run(cmd('LRANGE mylist3 0 -1')) == ["world1", "world2", "world3"]


def test_rpush_insert_multiple(server):
    assert server.run(cmd('RPUSH mylist4 "world" "world" "world"')) == 3
    assert server.run(cmd('RPUSH mylist4 "world" "world" "world"')) == 6

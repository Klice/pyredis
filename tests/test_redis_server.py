import pytest

from redis.redis_server import RedisServer


@pytest.fixture
def server():
    return RedisServer()


def test_ping(server):
    assert server.run(["PING"]) == "PONG"

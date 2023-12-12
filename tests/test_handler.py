

from redis.server import RedisRequestHandler


def test_ping():
    handler = RedisRequestHandler()
    handler.handle()

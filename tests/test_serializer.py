import pytest
from pyredis.serializer import RESPSerializer
from pyredis.redis_types import RedisError, SimpleString

messages = [
    ("$-1\r\n".encode('ascii'), None),
    ("*1\r\n$4\r\nping\r\n".encode('ascii'), ["ping"]),
    ("*2\r\n$4\r\necho\r\n$11\r\nhello world\r\n".encode('ascii'), ["echo", "hello world"]),
    ("*2\r\n$3\r\nget\r\n$3\r\nkey\r\n".encode('ascii'), ["get", "key"]),
    ("+OK\r\n".encode('ascii'), SimpleString("OK")),
    ("-Error message\r\n".encode('ascii'), RedisError("Error message")),
    ("$0\r\n\r\n".encode('ascii'), ""),
    ("+hello world\r\n".encode('ascii'), SimpleString("hello world")),
    ("$5\r\nhello\r\n".encode('ascii'), "hello"),
    (":1234\r\n".encode('ascii'), 1234),
    (":-1234\r\n".encode('ascii'), -1234),
    ("*2\r\n*3\r\n:1\r\n:2\r\n:3\r\n*2\r\n$5\r\nHello\r\n-World\r\n".encode('ascii'),
     [[1, 2, 3], ["Hello", RedisError("World")]])
]


@pytest.mark.parametrize("result,data", messages)
def test_messages_serialize(result, data):
    assert RESPSerializer.dump(data) == result

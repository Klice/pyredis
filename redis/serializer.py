
from redis.types import RedisError, SimpleString


class RESPSerializer:
    @classmethod
    def _encode(cls, data):
        res = []
        if data is None:
            res = ["$-1"]
        if isinstance(data, str):
            res = [f"${len(data)}", data]
        if isinstance(data, int):
            res = [f":{data}"]
        if isinstance(data, list):
            res = [f"*{len(data)}"]
            for d in data:
                res += cls._encode(d)
        if isinstance(data, RedisError):
            res = [f"-{data}"]
        if isinstance(data, SimpleString):
            res = [f"+{data}"]
        return res

    @classmethod
    def dump(cls, data):
        res = cls._encode(data)
        return ("\r\n".join(res)+"\r\n").encode('ascii')

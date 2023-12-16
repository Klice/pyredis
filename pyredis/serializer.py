
from pyredis.redis_types import RedisError, SimpleString


class RESPSerializer:
    @classmethod
    def _encode(cls, data):
        res = []
        if data is None:
            res.append("$-1")
        if isinstance(data, str) and not isinstance(data, SimpleString):
            res += [f"${len(data)}", data]
        if isinstance(data, int):
            res.append(f":{data}")
        if isinstance(data, list):
            res.append(f"*{len(data)}")
            for d in data:
                res += cls._encode(d)
        if isinstance(data, RedisError):
            res.append(f"-{data}")
        if isinstance(data, SimpleString):
            res.append(f"+{data}")
        return res

    @classmethod
    def dump(cls, data):
        res = cls._encode(data)
        return ("\r\n".join(res)+"\r\n").encode('ascii')

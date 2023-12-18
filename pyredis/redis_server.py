from datetime import datetime
from pyredis.redis_command_parser import RedisCommand
from pyredis.redis_types import RedisError, SimpleString


REDIS_COMMADS = {
    "PING": RedisCommand("PING"),
    "ECHO": RedisCommand("ECHO", ["value"]),
    "GET": RedisCommand("GET", ["key"]),
    "CONFIG": RedisCommand("CONFIG", allow_extra=True),
    "SET": RedisCommand(
        "SET",
        ["key", "value"],
        ["GET", ["NX", "XX"], ["KEEPTTL", "EX", "PX", "EXAT", "PXAT"]],
        {"EX": int, "PX": int, "EXAT": int, "PXAT": int}
    )
}


class RedisDataStore:
    data_store = {}

    def set(self, key, value, ts, ttl=None, is_get=False):
        ret = None
        if is_get:
            ret = self.get(key, ts)
        self.data_store[key] = {
            "value": value,
            "ttl": ttl,
        }
        return ret

    def get(self, key, ts):
        if key in self.data_store:
            if self.data_store[key]["ttl"] is not None and self.data_store[key]["ttl"] <= ts:
                del (self.data_store[key])
                return None
            return self.data_store[key]
        else:
            return None


class RedisTimesProvider():
    def get_time(self):
        dt = datetime.now()
        return datetime.timestamp(dt) * 1000


class RedisServer:
    data_store = RedisDataStore()

    def __init__(self, time_provider=RedisTimesProvider()):
        self.time_provider = time_provider

    def run(self, command_with_args):
        command = command_with_args[0]
        if command not in REDIS_COMMADS:
            return RedisError("Unknown command: " + " ".join(command_with_args))
        command_def = REDIS_COMMADS[command]
        command_dict = command_def.parse(command_with_args[1:])
        ruuner = getattr(self, f"_command_{command.lower()}")
        return ruuner(command_dict)

    def _command_ping(self, _):
        return SimpleString("PONG")

    def _command_echo(self, data):
        return data["value"]

    def _command_set(self, data):
        ts = self.time_provider.get_time()
        is_get = data.get("is_get", False)
        ttl = self._get_ttl(ts, data)
        if data.get("is_nx") and self.data_store.get(data["key"], ts):
            return SimpleString("OK")
        if data.get("is_xx") and not self.data_store.get(data["key"], ts):
            return SimpleString("OK")
        ret = self.data_store.set(data["key"], data["value"], ts, ttl=ttl, is_get=is_get)
        if is_get:
            return self._return_value(ret)
        else:
            return SimpleString("OK")

    def _command_get(self, data):
        ts = self.time_provider.get_time()
        return self._return_value(self.data_store.get(data["key"], ts))

    def _command_config(self, _):
        return SimpleString("")

    @staticmethod
    def _return_value(value):
        if value is None:
            return None
        else:
            return value.get("value")

    @staticmethod
    def _get_ttl(ts, data):
        ttl = None
        if "exat" in data:
            ttl = data["exat"] * 1000
        if "pxat" in data:
            ttl = data["pxat"]
        if "ex" in data:
            ttl = ts + data["ex"] * 1000
        if "px" in data:
            ttl = ts + data["px"]
        return ttl

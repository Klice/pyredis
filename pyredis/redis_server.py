from datetime import datetime
from pyredis.data_store import RedisDataStore
from pyredis.redis_command_parser import RedisCommand
from pyredis.redis_types import RedisError, SimpleString


REDIS_COMMANDS = {
    "PING": RedisCommand(),
    "ECHO": RedisCommand(["value"]),
    "GET": RedisCommand(["key"]),
    "CONFIG": RedisCommand(allow_extra=True),
    "SET": RedisCommand(
        ["key", "value"],
        ["GET", ["NX", "XX"], ["KEEPTTL", "EX", "PX", "EXAT", "PXAT"]],
        {"EX": int, "PX": int, "EXAT": int, "PXAT": int}
    ),
    "DEL": RedisCommand(["*key"]),
    "INCR": RedisCommand(["key"]),
    "DECR": RedisCommand(["key"]),
    "EXISTS": RedisCommand(["*key"]),
    "LPUSH": RedisCommand(["key", "*element"]),
    "RPUSH": RedisCommand(["key", "*element"]),
    "LRANGE": RedisCommand(["key", "start", "stop"]),
}


class RedisTimeProvider():
    def get_time(self):
        dt = datetime.now()
        return datetime.timestamp(dt) * 1000


class RedisServer:
    data_store = RedisDataStore()

    def __init__(self, time_provider=RedisTimeProvider()):
        self.time_provider = time_provider

    def run(self, command_with_args):
        command = command_with_args[0]
        if command not in REDIS_COMMANDS:
            return RedisError("Unknown command: " + " ".join(command_with_args))
        command_def = REDIS_COMMANDS[command]
        command_dict = command_def.parse(command_with_args[1:])
        runner = getattr(self, f"_command_{command.lower()}")
        try:
            return runner(command_dict)
        except Exception as e:
            return RedisError(str(e))

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

    def _command_del(self, data):
        return self.data_store.delete(data["key"])

    def _command_incr(self, data):
        return self._inrc_or_decr(data, 1)

    def _command_decr(self, data):
        return self._inrc_or_decr(data, -1)

    def _command_exists(self, data):
        res = 0
        for key in data["key"]:
            if self.data_store.exists(key):
                res += 1
        return res

    def _command_lpush(self, data):
        return self.data_store.lpush(data["key"], data["element"])

    def _command_rpush(self, data):
        return self.data_store.rpush(data["key"], data["element"])

    def _command_lrange(self, data):
        return self.data_store.lrange(data["key"], int(data["start"]), int(data["stop"]))

    def _inrc_or_decr(self, data, step):
        v = self._command_get(data)
        if v is None:
            v = 0
        try:
            new_val = int(v) + step
        except ValueError:
            return RedisError("value is not an integer or out of range")
        self._command_set({"key": data["key"], "value": str(new_val)})
        return new_val

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

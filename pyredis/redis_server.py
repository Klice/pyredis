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

    def set(self, key, value, is_get=False):
        ret = SimpleString("OK")
        if is_get:
            ret = self.data_store.get(key)
        self.data_store[key] = value
        return ret

    def get(self, key):
        if key in self.data_store:
            return self.data_store[key]
        else:
            return None


def store_set(data_store: RedisDataStore, *args):
    args_list = list(args)
    key = args_list.pop(0)
    value = args_list.pop(0)
    is_get = "GET" in args_list
    return data_store.set(key, value, is_get)


class RedisServer:
    data_store = RedisDataStore()

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
        if data.get("is_nx") and self.data_store.get(data["key"]):
            return SimpleString("OK")
        if data.get("is_xx") and not self.data_store.get(data["key"]):
            return SimpleString("OK")
        return self.data_store.set(data["key"], data["value"], data.get("is_get", False))

    def _command_get(self, data):
        return self.data_store.get(data["key"])

    def _command_config(self, _):
        return SimpleString("")

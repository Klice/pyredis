from pyredis.redis_types import RedisError, SimpleString


COMMANDS = {
    "PING": lambda _: SimpleString("PONG"),
    "ECHO": lambda _, x: x,
    "GET": lambda data_store, *args: data_store.get(args[0]),
    "SET": lambda data_store, *args: data_store.set(args[0], args[1]),
    "CONFIG": lambda _, *x: ""
}


class RedisDataStore:
    data_store = {}

    def set(self, key, value):
        self.data_store[key] = value
        return SimpleString("OK")

    def get(self, key):
        if key in self.data_store:
            return self.data_store[key]
        else:
            return None


class RedisServer:
    data_store = RedisDataStore()

    def run(self, command_with_args):
        command = command_with_args[0]
        if command not in COMMANDS:
            return RedisError("Unknown command: " + " ".join(command_with_args))
        args = command_with_args[1:]
        res = COMMANDS[command](self.data_store, *args)
        return res

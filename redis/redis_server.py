COMMANDS = {
    "PING": lambda: "PONG"
}


class RedisServer:
    def run(self, command_with_args):
        command = command_with_args[0]
        return COMMANDS[command]()

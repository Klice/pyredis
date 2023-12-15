class RedisError:
    message = None

    def __init__(self, message):
        self.message = message

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __str__(self) -> str:
        return self.message


class SimpleString(str):
    pass

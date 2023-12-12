from redis.types import RedisError


class RESPDeserializer:
    @classmethod
    def parse_array(cls, message):
        array_size, message = cls.parse_int(message)
        res = []
        for i in range(array_size):
            r, message = cls._parse(message)
            res.append(r)
        return res, message

    def parse_int(message):
        res = 0
        len = 0
        sign = 1
        if chr(message[0]) == "-":
            message = message[1:]
            sign = -1
        if chr(message[0]) == "+":
            message = message[1:]
        for b in message:
            len += 1
            if chr(b) == "\r":
                break
            res = res * 10 + int(chr(b))
        return res * sign, message[len+1:]

    def parse_simple_string(message):
        res = ""
        len = 0
        for b in message:
            len += 1
            if chr(b) == "\r":
                break
            res += chr(b)
        return res, message[len+1:]

    @classmethod
    def parse_bulk_string(cls, message):
        string_size, message = cls.parse_int(message)
        if string_size < 0:
            return None, message[2:]
        res = message[:string_size]
        return res.decode("ascii"), message[string_size+2:]

    @classmethod
    def _parse(cls, message):
        message_type = message[0]
        if message_type == 43:  # +
            return cls.parse_simple_string(message[1:])
        if message_type == 45:  # -
            res, message = cls.parse_simple_string(message[1:])
            return RedisError(res), message
        if message_type == 36:  # $
            return cls.parse_bulk_string(message[1:])
        if message_type == 58:  # :
            return cls.parse_int(message[1:])
        if message_type == ord("*"):
            return cls.parse_array(message[1:])

    @classmethod
    def load(cls, message):
        return cls._parse(message)[0]

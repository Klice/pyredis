from redis.deserializer import RESPDeserializer


class RequestProcessor:
    deserializer = RESPDeserializer

    def __init__(self, redis_server) -> None:
        self.server = redis_server

    def process_request(self, request):
        if request[0] != ord("*"):
            return self.server.run(request.decode("ascii").split(" "))
        else:
            return self.server.run(self.deserializer.load(request))

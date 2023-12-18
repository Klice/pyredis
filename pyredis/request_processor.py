from pyredis.deserializer import RESPDeserializer
from pyredis.redis_server import RedisServer
from pyredis.serializer import RESPSerializer


class RequestProcessor:
    deserializer = RESPDeserializer
    serializer = RESPSerializer

    def __init__(self, redis_server: RedisServer) -> None:
        self.server = redis_server

    def process_request(self, request):
        if request[0] != ord("*"):
            return (str(self.server.run(request.decode("ascii").split(" ")))+"\r\n").encode('ascii')
        else:
            return self.serializer.dump(self.server.run(self.deserializer.load(request)))

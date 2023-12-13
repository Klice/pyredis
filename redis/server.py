import socketserver
from redis.redis_server import RedisServer
from redis.request_processor import RequestProcessor


class RedisRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        self.request.sendall(RequestProcessor(RedisServer()).process_request(self.data))


class RedisTCPServer:
    def start(host, port):
        with socketserver.TCPServer((host, port), RedisRequestHandler) as server:
            server.serve_forever()

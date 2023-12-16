import logging
import socketserver
import sys
import threading
from redis.redis_server import RedisServer
from redis.request_processor import RequestProcessor

logger = logging.getLogger(__name__)


class RedisRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            cur_thread = threading.current_thread().name
            logger.debug(f"Thread: {cur_thread} Waiting for request...")
            self.data = self.request.recv(1024).strip()
            logger.debug(f"Thread: {cur_thread} Request: {self.data} from {self.client_address[0]}")
            if not self.data:
                logger.debug(f"Thread: {cur_thread} End of data")
                break
            res = RequestProcessor(RedisServer()).process_request(self.data)
            logger.debug(f"Thread: {cur_thread} Response: {res}")
            self.request.sendall(res)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class RedisTCPServer:
    def start(host, port):
        with ThreadedTCPServer((host, port), RedisRequestHandler) as server:
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                logger.info("Server Terminated")
                server.shutdown()
                sys.exit()

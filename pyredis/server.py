import logging
import socketserver
import sys
import threading
from pyredis.redis_server import RedisServer
from pyredis.request_processor import RequestProcessor

logger = logging.getLogger(__name__)


class RedisRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        cur_thread = threading.current_thread().name
        logger.info(f"{cur_thread}: New connection from {self.client_address[0]}:{self.client_address[1]}")
        while True:
            logger.debug(f"{cur_thread}: Waiting for request...")
            self.data = self.request.recv(1024)
            logger.debug(f"{cur_thread}: Request: {self.data} from {self.client_address[0]}")
            if not self.data:
                logger.info(f"{cur_thread}: {self.client_address[0]} disconnected")
                break
            res = RequestProcessor(RedisServer()).process_request(self.data)
            logger.debug(f"{cur_thread}: Response: {res}")
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

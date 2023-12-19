import logging
from pyredis.server import RedisTCPServer


def start_server():
    logging.basicConfig(level=logging.INFO)
    RedisTCPServer.start("localhost", 6379)


if __name__ == "__main__":
    start_server()

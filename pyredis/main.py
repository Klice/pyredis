import logging
from .server import RedisTCPServer


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)
    RedisTCPServer.start("localhost", 6379)

import logging
from pyredis.server import RedisTCPServer


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    RedisTCPServer.start("localhost", 6379)

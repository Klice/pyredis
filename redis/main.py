from redis.server import RedisTCPServer


if __name__ == "__main__":
    RedisTCPServer.start("localhost", 6379)

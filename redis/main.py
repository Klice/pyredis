from redis.server import RedisServer


if __name__ == "__main__":
    RedisServer.start("localhost", 9999)

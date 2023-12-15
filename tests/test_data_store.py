import pytest
from redis.redis_server import RedisDataStore


@pytest.fixture
def data_store():
    return RedisDataStore()


def test_set_get(data_store):
    data_store.set("key", "value")
    assert data_store.get("key") == "value"

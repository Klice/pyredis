import pytest
from pyredis.redis_server import RedisDataStore


@pytest.fixture
def data_store():
    return RedisDataStore()


def test_set_get(data_store):
    data_store.set("key", "value", 1)
    assert data_store.get("key", 1)["value"] == "value"
    assert data_store.get("key", 1)["ttl"] is None


def test_set_ttl(data_store):
    data_store.set("key", "value", 1, ttl=10)
    assert data_store.get("key", 1)["value"] == "value"
    assert data_store.get("key", 1)["ttl"] == 10


def test_set_ttl_expire(data_store):
    data_store.set("key", "value", 1, ttl=10)
    assert data_store.get("key", 1)["value"] == "value"
    assert data_store.get("key", 10) is None
    assert data_store.get("key", 1) is None

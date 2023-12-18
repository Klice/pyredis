import pytest

from pyredis.data_store import RedisDataStore


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


def test_del_one(data_store):
    assert data_store.delete(["key"]) == 0
    data_store.set("key", "value", 1)
    assert data_store.delete(["key"]) == 1
    assert data_store.get("key", 1) is None


def test_del_multiple(data_store):
    data_store.set("key1", "value", 1)
    data_store.set("key2", "value", 1)
    assert data_store.delete(["key1", "key2", "key3"]) == 2


def test_exists(data_store):
    data_store.set("key_exists", "value", 1)
    assert data_store.exists("key_exists") is True
    assert data_store.exists("key_nonexists") is False

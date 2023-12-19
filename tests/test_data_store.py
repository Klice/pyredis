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


def test_lpush(data_store):
    assert data_store.lpush("key_list", ["value1"]) == 1
    assert data_store.lpush("key_list", ["value2"]) == 2
    assert data_store.lpush("key_list", ["value2"]) == 3


def test_lpush_multiple(data_store):
    assert data_store.lpush("key_list2", ["value1", "value2", "value3"]) == 3
    assert data_store.lpush("key_list2", ["value1", "value2", "value3"]) == 6


def test_rpush(data_store):
    assert data_store.rpush("key_list_test_rpush", ["value1"]) == 1
    assert data_store.rpush("key_list_test_rpush", ["value2"]) == 2
    assert data_store.rpush("key_list_test_rpush", ["value2"]) == 3


def test_rpush_multiple(data_store):
    assert data_store.rpush("key_list_test_rpush_multiple", ["value1", "value2", "value3"]) == 3
    assert data_store.rpush("key_list_test_rpush_multiple", ["value1", "value2", "value3"]) == 6


def test_lrange(data_store):
    data_store.delete(["key_list2"])
    data_store.rpush("key_list2", ["value1", "value2", "value3", "value4", "value5", "value6"])
    assert data_store.lrange("key_list2", 0, -1) == ["value1", "value2", "value3", "value4", "value5", "value6"]
    assert data_store.lrange("key_list2", 0, -2) == ["value1", "value2", "value3", "value4", "value5"]
    assert data_store.lrange("key_list2", 2, -2) == ["value3", "value4", "value5"]
    assert data_store.lrange("key_list2", 2, 4) == ["value3", "value4", "value5"]
    assert data_store.lrange("key_list2", 0, 0) == ["value1"]


def test_lrange_wrong_type(data_store):
    data_store.set("key_list2", 1, 1)
    with pytest.raises(Exception) as ex_info:
        data_store.lrange("key_list2", 0, -1)
    assert "WRONGTYPE" in str(ex_info.value)


def test_lrange_nonexistent(data_store):
    data_store.delete(["key_list2"])
    assert data_store.lrange("key_list2", 0, -1) == []


def test_lrange_outofrange(data_store):
    data_store.delete(["key_list2"])
    data_store.rpush("key_list2", ["value1", "value2", "value3", "value4", "value5", "value6"])
    assert data_store.lrange("key_list2", 0, 10) == []
    assert data_store.lrange("key_list2", -100, 100) == []

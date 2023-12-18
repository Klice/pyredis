class RedisDataStore:
    data_store = {}

    def set(self, key, value, ts, ttl=None, is_get=False):
        ret = None
        if is_get:
            ret = self.get(key, ts)
        self.data_store[key] = {
            "value": value,
            "ttl": ttl,
        }
        return ret

    def get(self, key, ts):
        if key in self.data_store:
            if self.data_store[key]["ttl"] is not None and self.data_store[key]["ttl"] <= ts:
                del (self.data_store[key])
                return None
            return self.data_store[key]
        else:
            return None

    def delete(self, keys):
        keys_deleted = 0
        for key in keys:
            if key in self.data_store:
                del (self.data_store[key])
                keys_deleted += 1
        return keys_deleted

    def exists(self, key):
        return key in self.data_store

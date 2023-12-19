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

    def lpush(self, key, values):
        if key not in self.data_store:
            self.data_store[key] = []
        self.data_store[key] = values + self.data_store[key]
        return len(self.data_store[key])

    def rpush(self, key, values):
        if key not in self.data_store:
            self.data_store[key] = []
        self.data_store[key] = self.data_store[key] + values
        return len(self.data_store[key])

    def lrange(self, key, start, stop):
        if key not in self.data_store:
            return []
        if type(self.data_store[key]) is not list:
            raise Exception("WRONGTYPE Operation against a key holding the wrong kind of value")
        list_len = len(self.data_store[key])
        if abs(start) > list_len or abs(stop) > list_len:
            return []
        else:
            if stop == -1:
                stop = len(self.data_store[key])
            return self.data_store[key][start:stop+1]

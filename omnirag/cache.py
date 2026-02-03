import hashlib
from datetime import datetime, timedelta
class SimpleCache:
    def __init__(self, ttl_minutes=60):
        self.cache = {}
        self.ttl = timedelta(minutes=ttl_minutes)
    def _hash_key(self, query):
        return hashlib.md5(query.encode()).hexdigest()
    def get(self, query):
        key = self._hash_key(query)
        if key in self.cache:
            item = self.cache[key]
            if datetime.now() - item['timestamp'] < self.ttl:
                return item['result']
            else:
                del self.cache[key]
        return None
    def set(self, query, result):
        key = self._hash_key(query)
        self.cache[key] = {
            'result': result,
            'timestamp': datetime.now()
        }
    def clear(self):
        self.cache = {}
    def size(self):
        return len(self.cache)
    def stats(self):
        return {
            'size': len(self.cache),
            'ttl_minutes': self.ttl.total_seconds() / 60
        }

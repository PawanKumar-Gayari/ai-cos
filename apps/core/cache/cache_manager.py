from django.core.cache import cache


class CacheManager:

    @staticmethod
    def get(key):
        return cache.get(key)

    @staticmethod
    def set(key, value, timeout=300):
        cache.set(key, value, timeout)
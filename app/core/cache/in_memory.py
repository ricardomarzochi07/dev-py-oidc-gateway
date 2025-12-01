# in_memory.py
import time, asyncio
from typing import Any, Optional
from .base import Cache


class InMemoryCache(Cache):
    def __init__(self):
        self._data = {}  # key -> (value, expire_at|None)
        self._lock = asyncio.Lock()

    async def get(self, key: str):
        async with self._lock:
            item = self._data.get(key)
            if not item:
                return None
            value, exp = item
            if exp and exp < time.time():
                self._data.pop(key, None)
                return None
            return value

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        async with self._lock:
            expire_at = time.time() + ttl if ttl else None
            self._data[key] = (value, expire_at)
        return None  # 👈 deixa explícito p/ o type checker

    async def delete(self, key: str) -> None:
        async with self._lock:
            self._data.pop(key, None)
        return None

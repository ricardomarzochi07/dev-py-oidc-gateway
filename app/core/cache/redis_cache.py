# redis_cache.py
from typing import Any, Optional
from redis.asyncio import Redis
from .base import Cache


class RedisCache(Cache):
    def __init__(self, client: Redis):
        self.client = client

    async def get(self, key: str):
        return await self.client.get(key)

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        # Se usar decode_responses=True, value deve ser str/int/bytes
        await self.client.set(name=key, value=value, ex=ttl)
        return None  # 👈 explícito

    async def delete(self, key: str) -> None:
        await self.client.delete(key)
        return None

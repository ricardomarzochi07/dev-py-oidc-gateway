from redis.asyncio import Redis
from .in_memory import InMemoryCache
from .redis_cache import RedisCache
from .base import Cache
import os
from fastapi import Depends
from app.core.environment_config import AppConfig
from app.core.oidc_constants import Constants
from app.core.settings_config import load_config

_cache_instance: Cache | None = None
_redis_client: Redis | None = None


async def get_env() -> str:
    return os.getenv("APP_ENV", "LOCAL")


async def get_cache(config: AppConfig = Depends(load_config)) -> Cache:
    global _cache_instance, _redis_client
    if _cache_instance:
        return _cache_instance

    settings = config.oidc_gateway_env

    app_env = os.getenv("APP_ENV")
    if app_env == Constants.LOCAL_ENV:
        print("🔸 Usando cache InMemory (local)")
        _cache_instance = InMemoryCache()
    else:
        print("🔹 Usando cache Redis (dev/prod)")
        _redis_client = Redis.from_url(settings.redis_url, decode_responses=True)
        _cache_instance = RedisCache(_redis_client)

    return _cache_instance


async def shutdown_cache():
    global _redis_client
    if _redis_client:
        await _redis_client.close()

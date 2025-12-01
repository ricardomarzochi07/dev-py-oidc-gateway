# cache.py
from typing import Any, Protocol, Optional


class Cache(Protocol):
    async def get(self, key: str) -> Optional[Any]: ...

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None: ...

    async def delete(self, key: str) -> None: ...

from pydantic import BaseModel
from typing import Optional


class KeysDTO(BaseModel):
    public_key: Optional[bytes] = None
    private_key: Optional[bytes] = None

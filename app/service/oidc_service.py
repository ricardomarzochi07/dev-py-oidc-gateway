from abc import ABC, abstractmethod

from app.schemas.token_idp_schema import TokenIdpSchema
from app.schemas.token_internal_schema import TokenInternalSchema


class OidcService(ABC):

    @abstractmethod
    def generate_token_internal(self) -> TokenInternalSchema:
        pass

    @abstractmethod
    def generate_idp_token(self, internal_token: str) -> TokenIdpSchema:
        pass

    @abstractmethod
    def validate_token_internal(self, internal_token: str):
        pass
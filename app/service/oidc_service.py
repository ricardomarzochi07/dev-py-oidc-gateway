from abc import ABC, abstractmethod

from app.schemas.token_schema_response import TokenResponseSchema


class OidcService(ABC):

    @abstractmethod
    def generate_token(self) -> TokenResponseSchema:
        pass

    @abstractmethod
    def issue_wso2_token(self, internal_token: str) -> bool:
        pass

    @abstractmethod
    def validate_internal_token(self, internal_token: str):
        pass
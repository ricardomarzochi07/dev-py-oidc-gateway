from abc import ABC, abstractmethod
from buddybet_transactionmanager.http.transaction_http import HttpResponseSchema
from app.schemas.signupsubmit_request_schema import SignupSubmitRequest
from app.schemas.token_idp_schema import TokenIdpSchema
from app.schemas.token_internal_schema import TokenInternalSchema


class OidcTokenService(ABC):

    @abstractmethod
    def generate_token_internal(self) -> TokenInternalSchema:
        pass

    @abstractmethod
    def generate_idp_token(self, internal_token: str) -> TokenIdpSchema:
        pass

    @abstractmethod
    def _validate_token_internal(self, internal_token: str):
        pass

    @abstractmethod
    def _validate_token_idp_for_signup(self, idp_token: str):
        pass

    @abstractmethod
    def orchestrate_signup_user(self, data: SignupSubmitRequest) -> HttpResponseSchema:
        pass
from abc import ABC, abstractmethod
from buddybet_transactionmanager.http.transaction_http import HttpResponseSchema

from app.schemas.signin_init_request_schema import SigninInitRequestSchema
from app.schemas.signin_init_response_schema import SigninInitResponseSchema
from app.schemas.signupsubmit_request_schema import SignupSubmitRequest
from app.schemas.token_idp_schema import TokenIdpSchema
from app.schemas.token_internal_schema import TokenInternalSchema


class OidcTokenService(ABC):

    @abstractmethod
    def orchestrate_signup_user(self, data: SignupSubmitRequest) -> HttpResponseSchema:
        pass

    @abstractmethod
    def orchestrate_signin_init(self, data: SigninInitRequestSchema) -> SigninInitResponseSchema:
        pass
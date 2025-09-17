from buddybet_logmon_common.logger import get_logger
from app.clients.signupcore_service_service.signup_core_request_schema import SignupCoreRequest
from app.clients.signupcore_service_service.signupcore_paths import SignupCorePaths
from buddybet_transactionmanager.http.transaction_http import HttpClient
from buddybet_transactionmanager.http.transaction_http import HttpResponseSchema


class SignupCoreServiceClient:
    logger = get_logger()

    def register_in_signup_core(self, url_base: str, data: SignupCoreRequest, access_token: str) -> HttpResponseSchema:
        self.logger.info("Execute Request - post_register_user")
        try:
            signup_core_request = SignupCoreRequest(
                **data.dict(exclude={'jwt_nonce', 'jwt_csrf', 'captcha_token'}))

            headers = {"Authorization": f"Bearer {access_token}",
                       "Content-Type": "application/json"
            }
            client = HttpClient(url_base,
                                cert=None,
                                verify=False
                                )
            return client.post(path=SignupCorePaths.SIGNUP_USER,
                               headers=headers,
                               json_data=signup_core_request.dict)
        except Exception as e:
            self.logger.error("Unexpected error while preparing or sending request", exc_info=True)
            return HttpResponseSchema(
                status_response=False,
                status_code=500,
                data=None,
                message=f"Unhandled exception: {str(e)}"
            )

from buddybet_logmon_common.logger import get_logger
from buddybet_transactionmanager.schemas.http_response_schema import HttpResponseSchema
from app.clients.signupcore_service_service.signup_core_request_schema import SignupCoreRequest
from app.clients.signupcore_service_service.signupcore_paths import SignupCorePaths
from buddybet_transactionmanager.http.transaction_http import HttpClient

from app.core.exceptions import InvalidUserDataError, ResourceNotFoundError, ExternalServiceError, \
    UserAlreadyExistsError
from app.core.i18n_instance import i18n


class SignupCoreServiceClient:
    logger = get_logger()

    async def register_in_signup_core(self, url_base: str, data: SignupCoreRequest,
                                      access_token: str) -> HttpResponseSchema:
        self.logger.info("Execute Request - post_register_user")
        signup_core_request = SignupCoreRequest(
            **data.dict(exclude={'jwt_nonce', 'jwt_csrf', 'captcha_token'}))

        headers = {"Authorization": f"Bearer {access_token}",
                   "Content-Type": "application/json",
                   "Accept-Language": i18n.get_language()
                   }
        try:
            client = HttpClient(url_base, cert=None, verify=False)
            response = client.post(path=SignupCorePaths.SIGNUP_USER,
                                   headers=headers,
                                   json_data=signup_core_request.dict())
            if not response.status_response:
                if response.status_code == 400:
                    raise InvalidUserDataError()
                elif response.status_code == 404:
                    raise ResourceNotFoundError()
                elif response.status_code == 409:
                    raise UserAlreadyExistsError()
                else:
                    raise ExternalServiceError()
            return response

        except UserAlreadyExistsError:
            self.logger.warning("The user is already registered in the system..")
            raise
        except Exception as e:
            self.logger.error("Error de red al comunicar con Alta de Clientes", exc_info=True)
            raise ExternalServiceError() from e

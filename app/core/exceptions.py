class OidcValidationError(Exception):
    """Base class for JWT validation errors"""
    message_key = "invalid_token"  # default
    status_code = 401  # default para errores de autenticación

    def __init__(self, *args):
        super().__init__(*args)


class InvalidSignature(OidcValidationError):
    message_key = "invalid_signature"
    status_code = 401


class ExpiredToken(OidcValidationError):
    message_key = "expired_token"
    status_code = 401


class InvalidAudience(OidcValidationError):
    message_key = "invalid_audience"
    status_code = 403


class InvalidIssuer(OidcValidationError):
    message_key = "invalid_issuer"
    status_code = 403


class InvalidNotBefore(OidcValidationError):
    message_key = "invalid_not_before"
    status_code = 401


class InvalidClaims(OidcValidationError):
    message_key = "invalid_claims"
    status_code = 401


class InvalidToken(OidcValidationError):
    message_key = "invalid_token"
    status_code = 401


class JwtSigningError(OidcValidationError):
    message_key = "jwt_signing_error"
    status_code = 401


class ValidatorNotInitialized(OidcValidationError):
    message_key = "validator_not_initialized"
    status_code = 500


class ResourceNotFoundError(OidcValidationError):
    message_key = "resource_not_found"
    status_code = 404


class UserAlreadyExistsError(OidcValidationError):
    message_key = "user_already_exists"
    status_code = 409


class ExternalServiceError(OidcValidationError):
    message_key = "external_service_error"
    status_code = 502


class InvalidUserDataError(OidcValidationError):
    message_key = "invalid_user_data"
    status_code = 400


class ConnectionFailIdp(OidcValidationError):
    message_key = "connection_fail_idp"
    status_code = 502  # Bad Gateway


class InvalidScope(OidcValidationError):
    message_key = "invalid_scope"
    status_code = 403


class UserRegistrationError(OidcValidationError):
    message_key = "user_registration_error"
    status_code = 500


class External_Service_Error(OidcValidationError):
    message_key = "external_service_error"
    status_code = 503


class OidcValidationSuccess(Exception):
    """Base class for JWT validation errors"""
    message_key = "success_token"  # default
    status_code = 200  # default para errores de autenticación


class GenerateInternalToken(OidcValidationSuccess):
    message_key = "generate_internal_token"
    status_code = 200


class UserRegistration(OidcValidationSuccess):
    message_key = "user_registration"
    status_code = 200


"""

Excepción	            Código HTTP     Motivo

InvalidSignature	    401             Unauthorized	Firma no válida
ExpiredToken	        401             Unauthorized	Token caducado
InvalidAudience	        403             Forbidden	Público no autorizado
InvalidIssuer	        403             Forbidden	Emisor inválido
InvalidScope	        403             Forbidden	Scope no autorizado
ConnectionFailIdp	    502             Bad Gateway	Fallo al contactar el IDP
ValidatorNotInitialized	500             Internal Error	Error interno de configuración
JwtSigningError	500                     Internal Error	Error al firmar token

"""

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class AppError(Exception):
    """Базовая доменная ошибка. Ничего не знает про FastAPI, только код HTTP-статуса."""
    status_code = status.HTTP_400_BAD_REQUEST
    code = "app_error"
    message = "Request failed"

    def __init__(self, message: str | None = None, *, fields: dict[str, str] | None = None):
        self.message = message or self.message
        self.fields = fields or {}
        super().__init__(self.message)


class DuplicateUserError(AppError):
    status_code = status.HTTP_409_CONFLICT
    code = "duplicate_user"

    def __init__(self, field: str, message: str):
        super().__init__(message, fields={field: message})


class InvalidCredentialsError(AppError):
    status_code = status.HTTP_401_UNAUTHORIZED
    code = "invalid_credentials"
    message = "Incorrect login or password"


class AlreadyAuthenticatedError(AppError):
    status_code = status.HTTP_409_CONFLICT
    code = "already_authenticated"
    message = "Вы уже вошли в систему"


class NotAuthenticatedError(AppError):
    status_code = status.HTTP_401_UNAUTHORIZED
    code = "not_authenticated"
    message = "Not authenticated"


class AccountDisabledError(AppError):
    status_code = status.HTTP_403_FORBIDDEN
    code = "account_disabled"
    message = "User account is disabled"


class PermissionDeniedError(AppError):
    status_code = status.HTTP_403_FORBIDDEN
    code = "permission_denied"
    message = "Not enough permissions"


class BookNotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    code = "book_not_found"
    message = "Book not found"


async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"error": exc.code, "message": exc.message})

async def validation_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    fields = {}
    for err in exc.errors():
        loc = [part for part in err["loc"] if part not in ("body", "query", "path")]
        key = str(loc[-1]) if loc else "form"
        fields[key] = err["msg"].removeprefix("Value error, ")
    return JSONResponse(
        status_code=422,
        content={"error": "REQUEST_VALIDATION_ERROR", "message": "Invalid data", "fields": fields},
    )


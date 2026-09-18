from fastapi import HTTPException, status


class DuplicateUserError(HTTPException):
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            {"error": "duplicate_user", "field": field, "message": message},
        )


class AuthenticationError(HTTPException):
    def __init__(self, message: str = "Incorrect login or password"):
        super().__init__(
            status.HTTP_401_UNAUTHORIZED,
            {"error": "authentication_failed", "message": message},
        )


class AlreadyAuthenticatedError(HTTPException):
    def __init__(self, message: str = "Вы уже вошли в систему"):
        super().__init__(
            status.HTTP_409_CONFLICT,
            {"error": "already_authenticated", "message": message},
        )


class NotAuthenticatedError(HTTPException):
    def __init__(self, message: str = "User is not authenticated"):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            {"error": "not_authenticated", "message": message},
        )

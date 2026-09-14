from fastapi import HTTPException, status

class DuplicateUserError(HTTPException):
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(message)


class AuthenticationError(Exception):
    pass


class AlreadyAuthenticatedError(HTTPException):
    def __init__(self, message: str = "Вы уже вошли в систему"):
        super.__init__(status.HTTP_409_CONFLICT, {"error": "already_authenticated", "message": message})

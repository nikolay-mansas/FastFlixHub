from fastapi import Request
from jose import JWTError, jwt


def is_admin(request: Request) -> bool:
    ...


def get_user_cookie(indeficator: str, request: Request, ) -> str:
    ...

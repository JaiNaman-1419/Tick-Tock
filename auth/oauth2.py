from typing import Annotated
from config import JwtConfig
from jose import jwt, JWTError
from dotenv import load_dotenv

from os import environ as environ_var
from fastapi.security import OAuth2PasswordBearer
from fastapi import status, Depends, HTTPException
from datetime import timedelta, datetime, timezone


load_dotenv()


class Token:
    __SECRET_KEY = environ_var.get("SECRET_KEY")
    __ALGORITHM = JwtConfig().get_encoding_algorithm
    __OAUTH2_BEARER = OAuth2PasswordBearer(tokenUrl="auth/login")

    def create_access_token(
        self, username: str, user_id: int,
        is_admin: bool, expires_delta: timedelta
    ):
        encode = {
            "sub": username,
            "id": user_id,
            "is_admin": is_admin,
            "exp": datetime.now(timezone.utc) + expires_delta
        }

        return jwt.encode(encode, self.__SECRET_KEY, algorithm=self.__ALGORITHM)

    async def get_current_user(
        self,
        token: Annotated[str, Depends(__OAUTH2_BEARER)]
    ):
        try:
            payload = jwt.decode(
                token=token,
                key=self.__SECRET_KEY,
                algorithms=self.__ALGORITHM
            )

            username: str = payload.get("sub")
            user_id: int = payload.get("id")
            is_admin: str = payload.get("is_admin")

            if username is None or user_id is None:
                self.get_user_exception()

            return {
                "username": username,   
                "id": user_id,
                "is_admin": is_admin
            }

        except JWTError:
            self.get_user_exception()

    def get_user_exception(self):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

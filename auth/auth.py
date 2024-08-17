from models import Users
from .oauth2 import Token
from typing import Annotated
from database import Database
from datetime import timedelta

from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from validations import UserModel, TokenModel
from fastapi.security import OAuth2PasswordRequestForm

from fastapi import (
    status, APIRouter,
    Depends, HTTPException
)


ROUTER = APIRouter(prefix="/auth", tags=["AUTHENTICATION"])


@cbv(ROUTER)
class Authentication:
    LOGIN_FORM = Annotated[OAuth2PasswordRequestForm, Depends()]
    DB_DEPENDENCY = Annotated[Session, Depends(Database.get_db)]
    BCRYPT_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


    def authenticate_user(self, username: str, password: str, db):
        user = db.query(Users).filter(Users.username == username).first()
        if not user:
            return False
        if not self.BCRYPT_CONTEXT.verify(password, user.hashed_password):
            return False

        return user

    @ROUTER.post(
        path="/create-user",
        response_model=dict,
        status_code=status.HTTP_201_CREATED
    )
    async def create_user(
        self,
        db: DB_DEPENDENCY,
        create_user_request: UserModel
    ):
        try:
            create_user_model = Users(
                email = create_user_request.email,
                username = create_user_request.username,
                first_name = create_user_request.first_name,
                last_name = create_user_request.last_name,
                hashed_password = self.BCRYPT_CONTEXT.hash(create_user_request.password),
                is_admin = create_user_request.is_admin,
                is_active = True
            )
        
            db.add(create_user_model)
            db.commit()
        
            return {
                "msg": f"Hi, {create_user_model.first_name}!👋🏻\nLet's see how your day look like!😉"
            }

        except Exception as e:
            # db.query(Users).filter(Users.username == create_user_model.username).delete()
            # db.commit()
            print("--------------------------------ERROR-----------------------------------")
            print(e)
            print("------------------------------------------------------------------------") 

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error": str(e)
                }
            )

    @ROUTER.post("/login", response_model=TokenModel)
    async def login_for_access_token(self, form_data: LOGIN_FORM, db: DB_DEPENDENCY):
        user = self.authenticate_user(form_data.username, form_data.password, db)

        if not user:
            self.token_exception()

        token = Token().create_access_token(
            username=user.username,
            user_id=user.id,
            is_admin=user.is_admin,
            expires_delta=timedelta(minutes=20)
        )
        
        return {
            "access_token": token,
            "token_type": "bearer"
        }


    def token_exception(self):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

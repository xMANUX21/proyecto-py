from fastapi import Depends, HTTPException
from sqlmodel import Session
from app.auth.service import create_user, authenticate_user
from app.schemas.user_schema import UserCreate, UserLogin
from app.utils.dbConn import get_session
from app.utils.security import create_access_token


def register_controller(user_data: UserCreate, session: Session):
    return create_user(session, user_data)


def login_controller(data: UserLogin, session: Session):
    user = authenticate_user(session, data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
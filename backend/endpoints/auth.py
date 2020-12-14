"""
Содержит endpoints отвечающие за вход и выход пользователей
"""
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from core.config import database
from core.security import get_user_by_token, check_password

router = APIRouter()


@router.get("/logout")
async def logout(user: Dict = Depends(get_user_by_token)):
    """Разлогинивает пользователя"""
    await database.logout_user(user)

    return {"response": "ok"}


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Авторизует пользователя по стандарту OAuth2.0"""
    user = await database.get_by_username(form_data.username)

    if not user or not check_password(user.hashed_password, form_data.password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password"
        )

    token = await database.login_user(user.username)
    return {"access_token": token, "token_type": "bearer"}

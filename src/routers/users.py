# src/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.models.user import User, UserResponse  # SQLAlchemy модель
from src.models.schemas import UserBase  # Pydantic модель
from src.database import SessionLocal  # предполагается, что у вас есть функция для получения сессии БД
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import jwt
from dotenv import load_dotenv
import os


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username  # Возвращаем username как текущего пользователя
    except JWTError:
        raise credentials_exception


router = APIRouter()
load_dotenv(dotenv_path='E:/Rinh Hackathon/src/.env')


DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_users(db: Session, skip: int = 0):
    return db.query(User).offset(skip).all()

@router.get("/users", response_model=list[UserResponse], summary="Получить список всех пользователей")  # Используем Pydantic модель
def read_users(skip: int = 0, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    users = get_users(db, skip=skip)
    return users

import hashlib
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)  # Автоинкремент
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    role = Column(String)
    position = Column(String)
    department = Column(String)

    # Логин и пароль
    username = Column(String, unique=True, nullable=False)  # Логин пользователя
    password_hash = Column(String, nullable=False)  # Хэш пароля

    @validates('password_hash')
    def hash_password(self, key, password):
        """Хеширование пароля с использованием SHA-256 перед сохранением в базу"""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

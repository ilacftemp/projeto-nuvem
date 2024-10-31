# models.py
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Sequence
from database import Base

class UserRegister(BaseModel):
    nome: str
    email: str
    senha: str

class UserLogin(BaseModel):
    email: str
    senha: str

class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    nome = Column(String(50))
    email = Column(String(50), unique=True)
    hashed_password = Column(String(100))
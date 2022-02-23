from api.schemas.users import User
from pydantic import BaseModel, EmailStr


class LoginRequestBody(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    token: str
    user: User


class RegisterResponse(BaseModel):
    token: str
    user: User

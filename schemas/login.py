from typing import List, Optional
from pydantic import BaseModel
from schemas.user import UserSchema, ShowUser


class LoginSchema(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: ShowUser

class TokenData(BaseModel):
    email: Optional[str] = None
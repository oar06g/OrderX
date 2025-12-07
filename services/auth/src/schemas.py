from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True

class LoginInput(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    jwt: str
    
    class Config:
        from_attributes = True
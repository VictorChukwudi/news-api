import uuid
from pydantic import BaseModel, EmailStr, field_validator, ValidationInfo
from ..utils.enum import Role


class Register(BaseModel):
    
    model_config = {
        "from_attributes": True
    }
    
    first_name: str
    last_name: str
    email: EmailStr
    role: Role
    password: str
    confirm_password: str
    
    # @field_validator("confirm_password")
    # def check_passwords_match(cls, v, info: ValidationInfo):
    #     if "password" in info.data and v != info.data["password"]:
    #         raise ValueError("Passwords do not match")
    #     return v


class Login(BaseModel):
    model_config={
        "from_attributes": True
    }
    
    email: EmailStr
    password: str
  
    
class Show(BaseModel):
    
    model_config = {
        "from_attributes": True,
    }
    
    id: uuid.UUID
    first_name: str
    last_name: str
    email: str
    emailVerified: bool

class ShowUser(BaseModel):
    
    model_config = {
        "from_attributes": True,
    }
    status: str
    message: str
    data: Show
from pydantic import BaseModel

class RegisterSchema(BaseModel):
    companyName: str
    firstName:str
    lastName: str
    email: str
    password: str
    phoneNumber:str

class LoginSchema(BaseModel):
    email: str
    password: str
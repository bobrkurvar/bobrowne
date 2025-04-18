from pydantic import BaseModel

class UserInput(BaseModel):
    password: str
    username: str

class UserOutput(BaseModel):
    username: str
from pydantic import BaseModel

class Customer(BaseModel):
    user_name:str
    email:str

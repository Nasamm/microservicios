from pydantic import BaseModel

class Service(BaseModel):
    service_name:str
    description:str
    price:int

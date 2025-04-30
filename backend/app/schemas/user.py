from pydantic import BaseModel

class User(BaseModel):
    id: int
    userame: str
    email: str
    password: str

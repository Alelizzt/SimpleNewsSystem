from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    userame: str
    email: str
    password: str
    created_at: datetime = datetime.now()

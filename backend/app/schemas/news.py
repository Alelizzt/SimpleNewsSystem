from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class Section(str, Enum):  # Define un Enum explícito
    SPORTS = "sports"
    POLITICS = "politics"
    SOCIAL = "social"
    INTERNATIONAL = "international"
    CULTURE = "culture"
    HEALTH = "health"


class News(BaseModel):
    id: int
    title: str
    image: str
    content: str
    section: Section  # Usa el Enum como tipo
    author: str
    date_published: datetime = datetime.now()

class CreateNews(BaseModel):
    title: str
    image: str
    content: str
    section: Section  # Usa el Enum como tipo
    author: int
    date_published: datetime = datetime.now()


class UpdateNews(BaseModel):
    title: str = None
    image: str = None
    content: str = None
    section: Section = None
    author: int = None
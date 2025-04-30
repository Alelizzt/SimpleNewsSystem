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

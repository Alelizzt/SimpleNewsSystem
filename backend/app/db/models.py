from app.db.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Enum, Text
from datetime import datetime
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum  # Importa Enum de Python


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    news = relationship("News", backref="users", cascade="delete, merge")


# Define el Enum de Python para las secciones
class SectionEnum(str, PyEnum):
    SPORTS = "sports"
    POLITICS = "politics"
    SOCIAL = "social"
    INTERNATIONAL = "international"
    CULTURE = "culture"
    HEALTH = "health"


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    image = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    section = Column(Enum(SectionEnum), nullable=False)  # Usa el Enum de SQLAlchemy
    author_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False,
    )
    date_published = Column(DateTime, default=datetime.now, onupdate=datetime.now)

from typing import Optional
import uuid
import shutil
from pathlib import Path
from fastapi import HTTPException, status, UploadFile
from sqlalchemy.orm import Session
from app.db import models

UPLOAD_DIR = Path("uploads/images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def save_image(image: UploadFile) -> str:
    if image.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=400, detail="Invalid image format. Only JPEG and PNG are supported."
        )

    # Reemplazar espacios en el nombre del archivo por guiones bajos
    sanitized_filename = image.filename.replace(" ", "-")


    unique_filename = f"{uuid.uuid4()}_{sanitized_filename}"
    image_path = UPLOAD_DIR / unique_filename

    with image_path.open("wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    return str(image_path)

def create_news(news, image: UploadFile, db: Session):
    try:
        # Validar campos obligatorios
        if not news.title or not news.content or not news.section:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title, content, and section are required fields"
            )

        # Validar si ya existe una noticia con el mismo título
        existing_news = db.query(models.News).filter(models.News.title == news.title).first()
        if existing_news:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="A news article with this title already exists"
            )

        # Guardar la imagen
        image_path = save_image(image)

        # Crear la noticia
        section_value = news.section.value if isinstance(news.section, models.SectionEnum) else news.section
        new_news = models.News(
            title=news.title,
            content=news.content,
            author_id=news.author,
            image=image_path,
            section=section_value
        )
        db.add(new_news)
        db.commit()
        db.refresh(new_news)
        return new_news
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}"
        )


def get_news(news_id, db:Session):
    news = db.query(models.News).filter(models.News.id == news_id).first()
    if not news:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no news with the id {news_id}"
        )
    return news

def delete_news(news_id, db:Session):
    news = db.query(models.News).filter(models.News.id == news_id)
    if not news.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no news with the id {news_id} therefore is not eliminated"
        )
    news.delete(synchronize_session=False)
    db.commit()
    return {"response": "News deleted successfully!"}

def get_all_news(db: Session, page: int = 1, limit: int = 10):
    if page < 1:
        page = 1
    if limit < 1:
        limit = 10

    total = db.query(models.News).count()
    skip = (page - 1) * limit
    data = db.query(models.News).offset(skip).limit(limit).all()

    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No news found"
        )
    return {
        "news": data,
        "page": page,
        "limit": limit,
        "total": total,
    }

async def update_news(
    news_id: int,
    db: Session,
    title: Optional[str] = None,
    content: Optional[str] = None,
    section: Optional[str] = None,
    image: Optional[UploadFile] = None,
):
    news = db.query(models.News).filter(models.News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="News not found")

    if title is not None:
        news.title = title
    if content is not None:
        news.content = content
    if section is not None:
        news.section = section
    if image is not None:
        # Guarda la imagen en disco y actualiza el campo en la base de datos
        image_path = f"images/{image.filename}"
        with open(f"uploads/{image_path}", "wb") as buffer:
            buffer.write(await image.read())
        news.image = image_path

    db.commit()
    db.refresh(news)
    return {"response": "News updated successfully!"}

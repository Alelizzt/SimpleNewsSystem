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

def get_all_news(db:Session):
    data = db.query(models.News).all()
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No news found"
        )
    return data

def update_news(news_id, update_news, db:Session):
    news = db.query(models.News).filter(models.News.id == news_id)
    if not news.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no news with the id {news_id}"
        )
    news.update(update_news.dict(exclude_unset=True))
    db.commit()
    return {"response": "News updated successfully!"}

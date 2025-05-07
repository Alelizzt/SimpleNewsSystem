from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, Form
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.repository import news_service
from app.schemas.news import CreateNews, UpdateNews
from app.db.models import SectionEnum

router = APIRouter(prefix="/news", tags=["News"])


@router.post("/")
async def create_news(
    title: str = Form(...),
    content: str = Form(...),
    section: str = Form(...),
    author: int = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        section_enum = SectionEnum(section)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid section value. Allowed values are: {[e.value for e in SectionEnum]}"
        )

    news_data = CreateNews(
        title=title,
        content=content,
        section=section_enum,
        author=author,
        image=image.filename
    )
    return news_service.create_news(news_data, image, db)

@router.get("/")
def get_all_news(db: Session = Depends(get_db)):
    current_news = news_service.get_all_news(db)
    return current_news


@router.get("/{news_id}")
def get_news(news_id: int, db:Session = Depends(get_db)):
    news_found = news_service.get_news(news_id, db)
    return news_found


@router.delete("/{news_id}")
def delete_news(news_id: int, db: Session = Depends(get_db)):
    response = news_service.delete_news(news_id, db)
    return response


@router.patch("/{news_id}")
def update_news(
    news_id: int,
    update_new: UpdateNews,
    db:Session = Depends(get_db),
):
    response = news_service.update_news(news_id, update_new, db)
    return response

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, Form, status
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.repository import news_service
from app.schemas.news import CreateNews, UpdateNews
from app.schemas.user import User
from app.db.models import SectionEnum
from app.oauth import get_current_user

router = APIRouter(prefix="/news", tags=["News"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_news(
    title: str = Form(...),
    content: str = Form(...),
    section: str = Form(...),
    author: int = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        section_enum = SectionEnum(section)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid section value. Allowed values are: {[e.value for e in SectionEnum]}",
        )

    news_data = CreateNews(
        title=title,
        content=content,
        section=section_enum,
        author=author,
        image=image.filename,
    )
    return news_service.create_news(news_data, image, db)


@router.get("/", status_code=status.HTTP_200_OK)
def get_news_list(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return news_service.get_all_news(db, page=page, limit=limit)


@router.get("/{news_id}", status_code=status.HTTP_200_OK)
def get_news(news_id: int, db: Session = Depends(get_db)):
    news_found = news_service.get_news(news_id, db)
    return news_found


@router.delete("/{news_id}", status_code=status.HTTP_200_OK)
def delete_news(
    news_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    response = news_service.delete_news(news_id, db)
    return response


@router.patch("/{news_id}", status_code=status.HTTP_200_OK)
async def update_news(
    news_id: int,
    title: str = Form(None),
    content: str = Form(None),
    section: str = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await news_service.update_news(
        news_id=news_id,
        db=db,
        title=title,
        content=content,
        section=section,
        image=image
    )

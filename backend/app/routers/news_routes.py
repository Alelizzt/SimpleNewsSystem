from fastapi import APIRouter

from app.schemas.news import News

router = APIRouter(
    prefix="/news",
    tags=["News"]
)
@router.post("/")
def create_news(news: News):
    print(news)
    return True

@router.get("/")
def get_all_news():
    return {"message": "Get all news"}

@router.get("/{news_id}")
def get_news(news_id: int):
    return {"message": f"Get news with id {news_id}"}

@router.delete("/{news_id}")
def delete_news(news_id:int):
    return True

@router.patch('/{news_id}')
def update_news(news_id:int, update_new:News,):
    #update_user(news_id,update_new)
    return True

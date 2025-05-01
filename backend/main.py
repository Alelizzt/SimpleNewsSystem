from fastapi import FastAPI
import uvicorn
from app.routers import news_routes, user_routes

app = FastAPI()

app.include_router(user_routes.router)
app.include_router(news_routes.router)

# Usar el atribudo reload=True solo en ambiente de desarrollo
if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)

from fastapi import FastAPI
import uvicorn
from app.routers import auth_routes, news_routes, user_routes
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(user_routes.router)
app.include_router(news_routes.router)

app.include_router(auth_routes.router)

app.mount("/images", StaticFiles(directory="uploads/images"), name="images")

# Usar el atribudo reload=True solo en ambiente de desarrollo
if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)

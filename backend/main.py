from fastapi import FastAPI
import uvicorn
from app.routers import user, news


app = FastAPI()

app.include_router(user.router)
app.include_router(news.router)

# Usar el atribudo reload=True solo en ambiente de desarrollo
if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)

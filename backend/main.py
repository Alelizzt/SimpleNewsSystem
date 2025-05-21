from fastapi import FastAPI
import uvicorn
from app.routers import auth_routes, news_routes, user_routes
from fastapi.staticfiles import StaticFiles
from app.core.config import settings

description = """
Simple News API te ayuda a gestionar y consultar noticias. 🌐

### Endpoints principales

#### 📰 Noticias (`/news`)
- **Leer noticias públicas**: `GET /news/`
- **Crear noticia**: `POST /news/` _(requiere autenticación)_
- **Actualizar noticia**: `PUT /news/{id}` _(requiere autenticación)_
- **Eliminar noticia**: `DELETE /news/{id}` _(requiere autenticación)_

#### 👤 Usuarios y Periodistas (`/users`)
- **Registrar usuario**: `POST /users/`
- **Leer usuarios**: `GET /users/` _(requiere autenticación)_
- **Actualizar usuario**: `PUT /users/{id}` _(requiere autenticación)_
- **Eliminar usuario**: `DELETE /users/{id}` _(requiere autenticación)_

#### 🔑 Autenticación (`/login`)
- **Iniciar sesión**: `POST /login/`
  Envía tus credenciales (`username` y `password`) para obtener un token JWT.
- Usa el token JWT en el header:
  `Authorization: Bearer <token>`

---

**Notas:**
- Los endpoints protegidos requieren autenticación con JWT.
- Puedes subir imágenes para las noticias usando el endpoint de creación.
- Accede a `/docs` para probar la API de forma interactiva.

"""

API_VERSION_PREFIX = f"/v{settings.PROJECT_VERSION.split('.')[0]}"

app = FastAPI(
    title="Simple web news API",
    description=description,
    version=settings.PROJECT_VERSION,
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Alejandro Lizzt",
        "url": "https://github.com/Alelizzt/",
        "email": "email@example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

app.include_router(user_routes.router, prefix=API_VERSION_PREFIX)
app.include_router(news_routes.router, prefix=API_VERSION_PREFIX)

app.include_router(auth_routes.router, prefix=API_VERSION_PREFIX)

app.mount(f"{API_VERSION_PREFIX}/images", StaticFiles(directory="uploads/images"), name="images")

# Usar el atribudo reload=True solo en ambiente de desarrollo
if __name__ == "__main__":
    #uvicorn.run("main:app", port=8000, reload=True)
    uvicorn.run("main:app", port=8000)

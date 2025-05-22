# Simple News System - Backend

API para la gestión y consulta de noticias, usuarios y autenticación JWT, desarrollada con **FastAPI** y **SQLAlchemy**.

---

## 🚀 Requisitos

- Python 3.10+
- PostgreSQL (o [Docker](https://www.docker.com/))
- [uv](https://docs.astral.sh/uv/) para la gestión de paquetes y entornos de Python.

---

## ⚙️ Instalación

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/tu_usuario/SimpleNewsSystem.git
   cd SimpleNewsSystem/backend
   ```

2. **Crea el entorno virtual e instala las dependencias:**
   Por defecto, las dependencias se gestionan con [uv](https://docs.astral.sh/uv/), ve allí e instálalas. Desde `./backend/` puedes instalar todas las dependencias con:
   ```console
   $ uv sync
   ```

3. **Activa el entorno virtual:**
   ```bash
   .venv\Scripts\activate   # En Windows
   source .venv/bin/activate  # En Linux/Mac
   ```
   Asegúrate de que tu editor está utilizando el entorno virtual Python correcto, con el intérprete en `backend/.venv/bin/python`.

4. **Configura la base de datos:**
   - Crea una base de datos en PostgreSQL.
   - Si utilizas tu propia base de datos ajusta los parámetros de conexión en `app/core/config.py`, o si lo prefieres, edita el fichero `.env` con las configuraciones que utiliza docker.
   - **Configura la versión de la API** agregando en tu `.env`:
     ```
     PROJECT_VERSION=1.1.0
     ```

5. **Realiza las migraciones (si usas Alembic):**
   ```bash
   alembic upgrade head
   ```

---

## ▶️ Ejecución

```bash
uvicorn main:app --reload
```
- Accede a la API en: [http://localhost:8000](http://localhost:8000)
- Documentación interactiva: [http://localhost:8000/docs](http://localhost:8000/docs)

Si deseas ejecutar el proyecto en un ambiente de producción se recomienda utilizar:
```bash
uvicorn main:app
```
---

## 📝 Endpoints principales

- **/v1/news/**: CRUD de noticias (protegido con JWT para crear, actualizar y eliminar)
- **/v1/users/**: Registro y gestión de usuarios
- **/v1/login/**: Autenticación y obtención de token JWT

---

## 🔒 Autenticación

- Para endpoints protegidos, inicia sesión en `/v1/login/` y usa el token JWT en el header:
  ```
  Authorization: Bearer <token>
  ```

---

## 📦 Estructura del proyecto

```
backend/
│
├── app/
│   ├── db/
│   ├── repository/
│   ├── routers/
│   ├── schemas/
│   ├── oauth.py
│   └── token.py
├── uploads/
├── main.py
├── requirements.txt
└── README.md
```

---

## 🖼️ Subida de imágenes

- Las imágenes de noticias se guardan en la carpeta `uploads/images/`.
- Usa el endpoint `POST /v1/news/` para subir una noticia con imagen.

---

## 🛠️ Notas de desarrollo

- Puedes modificar la configuración de la API y la versión en `main.py` y `.env`.
- Los ejemplos de uso de los modelos aparecen en la documentación Swagger.

---

## 📄 Licencia

Este proyecto está bajo la licencia Apache 2.0.

---

**Desarrollado por Alejandro Lizzt**
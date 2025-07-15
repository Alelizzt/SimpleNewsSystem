# SimpleNewsSystem

Sistema completo para la publicación y gestión de noticias, compuesto por un backend (API REST) y un frontend (cliente web).

---

## 🚀 Características principales

- Gestión de noticias, usuarios y autenticación JWT.
- Subida de imágenes asociadas a noticias.
- Interfaz web moderna y fácil de usar.
- Arquitectura desacoplada: backend en FastAPI y frontend en Vite + React/Vue.

---

## 📦 Estructura del proyecto

```
SimpleNewsSystem/
│
├── backend/      # API REST (FastAPI, SQLAlchemy, PostgreSQL)
│   └── README.md
├── frontend/     # Cliente web (Vite + React/Vue)
│   └── README.md
├── docker-compose.yml
└── README.md     # Este archivo
```

---

## 🛠️ Desarrollo local

Puedes levantar tu propia base de datos PostgreSQL y configurar los valores en el archivo `.env`.
Alternativamente, puedes usar Docker para iniciar la base de datos:

```bash
docker-compose up -d db
```

Luego, sigue las instrucciones específicas para cada capa:

- [Backend](./backend/README.md)
- [Frontend](./frontend/simple-news/README.md)

---

## 🚢 Despliegue del proyecto completo

Para desplegar todo el sistema (backend, frontend y base de datos) con Docker, ejecuta:

```bash
docker-compose up --build -d
```

---

## 📄 Documentación

Consulta los README de cada capa para instrucciones detalladas de instalación, configuración y uso:

- [Backend](./backend/README.md)
- [Frontend](./frontend/README.md)

---

## 📝 Licencia

Este proyecto está bajo la licencia Apache 2.0.

---

**Desarrollado con ❤️ por [Tu Nombre]**
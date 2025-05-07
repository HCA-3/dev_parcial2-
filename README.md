# 🚀 API de Usuarios y Tareas con FastAPI

# API de Usuarios y Tareas

API básica para gestión de usuarios y sus tareas, desarrollada con FastAPI y SQLAlchemy.

## Características principales

- ✅ CRUD completo para usuarios
- ✅ CRUD completo para tareas
- ✅ Relación uno-a-muchos entre usuarios y tareas
- ✅ Validación de datos con Pydantic
- ✅ Documentación automática (Swagger UI)

## Requisitos

- Python 3.7+
- Pip

## Instalación

1. Clonar el repositorio:
```bash
git clone [url-del-repositorio]
cd [nombre-del-directorio]

## Instalar dependencias

- pip install -r requirements.txt


## Configurar base de datos (SQLite por defecto)

- La base de datos se creará automáticamente al iniciar la aplicación

## Ejecución

- uvicorn main:app --reload
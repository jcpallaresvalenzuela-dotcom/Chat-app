# Chat App - NOIC

Aplicación de chat en tiempo real construida con FastAPI y WebSockets.

## Características

- Chat en tiempo real con WebSockets
- Máximo 2 jugadores por sala
- Interfaz tipo terminal minimalista

## Arquitectura de la aplicación

┌─────────────────┐    WebSocket    ┌─────────────────┐
│   Frontend      │ ◄──────────────►│    Backend      │
│   (Browser)     │                 │   (Python)      │
│                 │                 │                 │
│ • HTML          │                 │ • FastAPI       │
│ • CSS           │                 │ • WebSockets    │
│ • JavaScript    │                 │ • Lógica de chat│
└─────────────────┘                 └─────────────────┘

## Estructura del Proyecto

```
Chat-app/
├── app.py              # Servidor FastAPI
├── requirements.txt    # Dependencias de Python
├── templates/
│   └── index.html     # Interfaz del chat
├── Dockerfile         # Configuración de Docker
├── docker-compose.yml # Orquestación de contenedores
└── .dockerignore      # Archivos excluidos del build
```

## Uso con Docker

### Opción 1: Docker Compose (Recomendado)

```bash
# Construir y ejecutar
docker-compose up --build

# Ejecutar en segundo plano
docker-compose up -d

# Detener
docker-compose down
```

### Opción 2: Docker CLI

```bash
# Construir la imagen
docker build -t chat-app .

# Ejecutar el contenedor
docker run -p 8000:8000 chat-app

# Ejecutar en segundo plano
docker run -d -p 8000:8000 --name chat-container chat-app

# Detener el contenedor
docker stop chat-container
docker rm chat-container
```

## Acceso

Una vez ejecutada la aplicación:

- **URL**: http://localhost:8000
- **Puerto**: 8000

## Dependencias

- FastAPI 0.111.0
- Uvicorn 0.30.1
- Jinja2 3.1.4

## Desarrollo Local

Si prefieres ejecutar sin Docker:

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
uvicorn app:app --reload
```

## Notas de Seguridad

- La aplicación se ejecuta como usuario no-root dentro del contenedor
- Solo se expone el puerto 8000
- Health checks incluidos para monitoreo

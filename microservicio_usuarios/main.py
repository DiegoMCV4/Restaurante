# Microservicio de Usuarios - Sistema de Restaurante
from fastapi import FastAPI
from infrastructure.api.user_controller import router
import uvicorn

app = FastAPI(
    title="Microservicio de Usuarios",
    description="API para gestionar usuarios del restaurante - Arquitectura Hexagonal",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(router)

@app.get("/", tags=["Root"])
def root():
    return {
        "mensaje": "Microservicio de Usuarios del Restaurante",
        "version": "1.0.0",
        "documentacion": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)

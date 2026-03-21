# Microservicio de Clientes - Sistema de Restaurante
from fastapi import FastAPI
from infrastructure.api.user_controller import router
import uvicorn

app = FastAPI(
    title="Microservicio de Clientes",
    description="API para gestionar clientes del restaurante - Arquitectura Hexagonal",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(router)

@app.get("/", tags=["Root"])
def root():
    return {
        "mensaje": "Microservicio de Clientes del Restaurante",
        "version": "1.0.0",
        "documentacion": "/docs"
    }

@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "ok",
        "service": "clientes",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)

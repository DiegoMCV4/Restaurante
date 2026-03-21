# Microservicio de Pedidos - Sistema de Restaurante
from fastapi import FastAPI
from infrastructure.api.order_controller import router
import uvicorn

app = FastAPI(
    title="Microservicio de Pedidos",
    description="API para gestionar pedidos del restaurante - Arquitectura Hexagonal",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(router)

@app.get("/", tags=["Root"])
def root():
    return {
        "mensaje": "Microservicio de Pedidos del Restaurante",
        "version": "1.0.0",
        "documentacion": "/docs"
    }

@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "ok",
        "service": "pedidos",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)

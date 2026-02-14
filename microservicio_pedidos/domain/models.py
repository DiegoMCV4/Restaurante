# Modelo de dominio para Pedido
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Pedido(BaseModel):
    """Modelo de dominio para representar un Pedido del restaurante"""
    idpedido: int
    idusuario: int
    descripcion: str
    estado: str  # Ejemplo: "pendiente", "en_preparacion", "entregado", "cancelado"
    fecha: str
    total: float
    
    class Config:
        json_schema_extra = {
            "example": {
                "idpedido": 1,
                "idusuario": 1,
                "descripcion": "Pizza Margarita y Coca Cola",
                "estado": "pendiente",
                "fecha": "2026-02-13 14:30:00",
                "total": 25.50
            }
        }

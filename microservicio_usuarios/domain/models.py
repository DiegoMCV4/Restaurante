# Modelo de dominio para Usuario
from pydantic import BaseModel, EmailStr
from typing import Optional

class Usuario(BaseModel):
    """Modelo de dominio para representar un Usuario del restaurante"""
    idusuario: int
    nombre: str
    email: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "idusuario": 1,
                "nombre": "Juan Pérez",
                "email": "juan@ejemplo.com"
            }
        }

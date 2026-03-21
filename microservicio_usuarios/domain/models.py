# Modelo de dominio para Cliente
from pydantic import BaseModel, EmailStr, Field

class Cliente(BaseModel):
    """Modelo de dominio para representar un Cliente del restaurante"""
    idcliente: int = Field(gt=0)
    nombre: str = Field(min_length=2, max_length=120)
    cel: str = Field(pattern=r"^\+?[0-9]{7,15}$")
    email: EmailStr
    
    class Config:
        json_schema_extra = {
            "example": {
                "idcliente": 1,
                "nombre": "Juan Pérez",
                "cel": "555123456",
                "email": "juan@ejemplo.com"
            }
        }


class ClienteEncolado(BaseModel):
    """Respuesta cuando un cliente es encolado en RabbitMQ."""
    mensaje: str
    idcliente: int

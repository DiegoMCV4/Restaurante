# Modelo de dominio para Pedido
from pydantic import BaseModel, Field, model_validator

class Pedido(BaseModel):
    """Modelo de dominio para representar un Pedido del restaurante"""
    idpedido: int = Field(gt=0)
    descripcion: str = Field(min_length=3, max_length=500)
    nombre_pedido: str = Field(min_length=1, max_length=255)
    cantidad: int = Field(ge=1)
    precio: float = Field(gt=0)
    idcliente: int = Field(gt=0)
    total: float | None = Field(default=None, ge=0)

    @model_validator(mode="after")
    def calcular_total(self):
        # El total siempre se recalcula para evitar inconsistencias.
        self.total = round(self.cantidad * self.precio, 2)
        return self
    
    class Config:
        json_schema_extra = {
            "example": {
                "idpedido": 1,
                "descripcion": "Pizza familiar con extra queso",
                "nombre_pedido": "Pizza familiar mitad pepperoni mitad hawaiana",
                "cantidad": 2,
                "precio": 12.50,
                "idcliente": 1,
                "total": 25.00,
            }
        }


class PedidoEncolado(BaseModel):
    """Respuesta al registrar pedido en cola."""
    mensaje: str
    idpedido: int

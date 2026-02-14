# Controlador API para el microservicio de Pedidos
from fastapi import APIRouter, HTTPException, status
from typing import List
from domain.models import Pedido
from infrastructure.adapters.order_repository_impl import RepositorioPedidoImpl
from application.services.order_service import ServicioPedido

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])
repo = RepositorioPedidoImpl()
servicio = ServicioPedido(repo)

@router.post("/", response_model=Pedido, status_code=status.HTTP_201_CREATED)
def crear_pedido(pedido: Pedido):
    """Registrar un nuevo pedido en el sistema"""
    return servicio.crear(pedido)

@router.get("/", response_model=List[Pedido])
def listar_pedidos():
    """Consultar todos los pedidos registrados"""
    return servicio.obtener_todos()

@router.get("/{idpedido}", response_model=Pedido)
def obtener_pedido(idpedido: int):
    """Consultar información de un pedido específico"""
    pedido = servicio.obtener_por_id(idpedido)
    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pedido con ID {idpedido} no encontrado"
        )
    return pedido

@router.put("/{idpedido}", response_model=Pedido)
def actualizar_pedido(idpedido: int, pedido: Pedido):
    """Modificar un pedido existente"""
    pedido_actualizado = servicio.actualizar(idpedido, pedido)
    if not pedido_actualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pedido con ID {idpedido} no encontrado"
        )
    return pedido_actualizado

@router.delete("/{idpedido}", status_code=status.HTTP_200_OK)
def eliminar_pedido(idpedido: int):
    """Eliminar un pedido del sistema"""
    eliminado = servicio.eliminar(idpedido)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pedido con ID {idpedido} no encontrado"
        )
    return {"mensaje": f"Pedido con ID {idpedido} eliminado exitosamente"}

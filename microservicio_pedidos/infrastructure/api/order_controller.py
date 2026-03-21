# Controlador API para el microservicio de Pedidos
from fastapi import APIRouter, HTTPException, status
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from domain.models import Pedido, PedidoEncolado
from infrastructure.adapters.order_repository_impl import RepositorioPedidoImpl
from infrastructure.adapters.cliente_cache_repository_impl import ClienteCacheRepositoryImpl
from infrastructure.messaging.rabbitmq_publisher import RabbitMQPedidoPublisher
from application.services.order_service import ServicioPedido

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])
repo = RepositorioPedidoImpl()
servicio = ServicioPedido(repo)
publisher = RabbitMQPedidoPublisher()
cache_clientes = ClienteCacheRepositoryImpl()

@router.get("/health/db", tags=["Health"])
def health_db_pedidos():
    """Comprueba que el servicio puede conectarse a MySQL."""
    try:
        repo.ping()
        return {"status": "ok", "database": "mysql"}
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Base de datos de pedidos no disponible",
        )

@router.get("/health/broker", tags=["Health"])
def health_broker_pedidos():
    """Comprueba que el servicio puede conectarse a RabbitMQ."""
    try:
        publisher.ping()
        return {"status": "ok", "broker": "rabbitmq"}
    except RuntimeError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Broker RabbitMQ no disponible",
        )


@router.post("/", response_model=PedidoEncolado, status_code=status.HTTP_202_ACCEPTED)
def crear_pedido(pedido: Pedido):
    """Encola un nuevo pedido para persistencia asíncrona.

    Valida que el cliente exista en la caché MySQL antes de encolar.
    """
    if servicio.obtener_por_id(pedido.idpedido):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un pedido con ID {pedido.idpedido}",
        )
    if not cache_clientes.existe(pedido.idcliente):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"El cliente con ID {pedido.idcliente} no existe en el sistema",
        )
    try:
        publisher.publicar_pedido_creado(pedido.model_dump())
        return {
            "mensaje": "Pedido encolado correctamente",
            "idpedido": pedido.idpedido,
        }
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc

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

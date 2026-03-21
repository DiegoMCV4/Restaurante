# Controlador API para el microservicio de Clientes
from fastapi import APIRouter, HTTPException, status
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from domain.models import Cliente, ClienteEncolado
from infrastructure.adapters.user_repository_impl import RepositorioClientePostgres
from infrastructure.messaging.rabbitmq_publisher import RabbitMQClientePublisher
from application.services.user_service import ServicioCliente

router = APIRouter(prefix="/clientes", tags=["Clientes"])
repo = RepositorioClientePostgres()
servicio = ServicioCliente(repo)
publisher = RabbitMQClientePublisher()

@router.get("/health/db", tags=["Health"])
def health_db_clientes():
    """Comprueba que el servicio puede conectarse a PostgreSQL."""
    try:
        repo.ping()
        return {"status": "ok", "database": "postgres"}
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Base de datos de clientes no disponible",
        )

@router.get("/health/broker", tags=["Health"])
def health_broker_clientes():
    """Comprueba que el servicio puede conectarse a RabbitMQ."""
    try:
        publisher.ping()
        return {"status": "ok", "broker": "rabbitmq"}
    except RuntimeError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Broker RabbitMQ no disponible",
        )


@router.post("/", response_model=ClienteEncolado, status_code=status.HTTP_202_ACCEPTED)
def crear_cliente(cliente: Cliente):
    """Encola un nuevo cliente para persistencia asíncrona."""
    if servicio.obtener_por_id(cliente.idcliente):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un cliente con ID {cliente.idcliente}",
        )
    if servicio.obtener_por_cel(cliente.cel):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un cliente con teléfono {cliente.cel}",
        )
    try:
        publisher.publicar_cliente_creado(cliente.model_dump())
        return {
            "mensaje": "Cliente encolado correctamente",
            "idcliente": cliente.idcliente,
        }
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc

@router.get("/", response_model=List[Cliente])
def listar_clientes():
    """Consultar todos los clientes registrados"""
    return servicio.obtener_todos()

@router.get("/{idcliente}", response_model=Cliente)
def obtener_cliente(idcliente: int):
    """Consultar información de un cliente específico"""
    cliente = servicio.obtener_por_id(idcliente)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente con ID {idcliente} no encontrado"
        )
    return cliente

@router.put("/{idcliente}", response_model=Cliente)
def actualizar_cliente(idcliente: int, cliente: Cliente):
    """Modificar datos de un cliente existente"""
    cliente_por_cel = servicio.obtener_por_cel(cliente.cel)
    if cliente_por_cel and cliente_por_cel.idcliente != idcliente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un cliente con teléfono {cliente.cel}",
        )
    try:
        cliente_actualizado = servicio.actualizar(idcliente, cliente)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
    if not cliente_actualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente con ID {idcliente} no encontrado"
        )
    return cliente_actualizado

@router.delete("/{idcliente}", status_code=status.HTTP_200_OK)
def eliminar_cliente(idcliente: int):
    """Eliminar un cliente del sistema"""
    eliminado = servicio.eliminar(idcliente)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente con ID {idcliente} no encontrado"
        )
    return {"mensaje": f"Cliente con ID {idcliente} eliminado exitosamente"}

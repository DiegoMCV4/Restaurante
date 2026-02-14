# Controlador API para el microservicio de Usuarios
from fastapi import APIRouter, HTTPException, status
from typing import List
from domain.models import Usuario
from infrastructure.adapters.user_repository_impl import RepositorioUsuarioImpl
from application.services.user_service import ServicioUsuario

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])
repo = RepositorioUsuarioImpl()
servicio = ServicioUsuario(repo)

@router.post("/", response_model=Usuario, status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: Usuario):
    """Registrar un nuevo usuario en el sistema"""
    return servicio.crear(usuario)

@router.get("/", response_model=List[Usuario])
def listar_usuarios():
    """Consultar todos los usuarios registrados"""
    return servicio.obtener_todos()

@router.get("/{idusuario}", response_model=Usuario)
def obtener_usuario(idusuario: int):
    """Consultar información de un usuario específico"""
    usuario = servicio.obtener_por_id(idusuario)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {idusuario} no encontrado"
        )
    return usuario

@router.put("/{idusuario}", response_model=Usuario)
def actualizar_usuario(idusuario: int, usuario: Usuario):
    """Modificar nombre o email de un usuario existente"""
    usuario_actualizado = servicio.actualizar(idusuario, usuario)
    if not usuario_actualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {idusuario} no encontrado"
        )
    return usuario_actualizado

@router.delete("/{idusuario}", status_code=status.HTTP_200_OK)
def eliminar_usuario(idusuario: int):
    """Eliminar un usuario del sistema"""
    eliminado = servicio.eliminar(idusuario)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {idusuario} no encontrado"
        )
    return {"mensaje": f"Usuario con ID {idusuario} eliminado exitosamente"}

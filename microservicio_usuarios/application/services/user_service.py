# Servicio de aplicación para Usuarios
from typing import List, Optional
from domain.models import Usuario
from application.ports.user_repository import RepositorioUsuario

class ServicioUsuario:
    """Servicio de aplicación que contiene la lógica de negocio de usuarios"""
    
    def __init__(self, repositorio: RepositorioUsuario):
        self.repositorio = repositorio
    
    def crear(self, usuario: Usuario) -> Usuario:
        """Registra un nuevo usuario en el sistema"""
        return self.repositorio.crear(usuario)
    
    def obtener_todos(self) -> List[Usuario]:
        """Consulta todos los usuarios registrados"""
        return self.repositorio.obtener_todos()
    
    def obtener_por_id(self, idusuario: int) -> Optional[Usuario]:
        """Consulta la información de un usuario específico"""
        return self.repositorio.obtener_por_id(idusuario)
    
    def actualizar(self, idusuario: int, usuario: Usuario) -> Optional[Usuario]:
        """Modifica el nombre o email de un usuario existente"""
        return self.repositorio.actualizar(idusuario, usuario)
    
    def eliminar(self, idusuario: int) -> bool:
        """Elimina un usuario del sistema"""
        return self.repositorio.eliminar(idusuario)

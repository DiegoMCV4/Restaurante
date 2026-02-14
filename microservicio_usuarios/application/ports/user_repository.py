# Puerto (interfaz) del repositorio de Usuarios
from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models import Usuario

class RepositorioUsuario(ABC):
    """Interfaz del repositorio de usuarios siguiendo arquitectura hexagonal"""
    
    @abstractmethod
    def crear(self, usuario: Usuario) -> Usuario:
        """Crea un nuevo usuario"""
        pass
    
    @abstractmethod
    def obtener_todos(self) -> List[Usuario]:
        """Obtiene todos los usuarios"""
        pass
    
    @abstractmethod
    def obtener_por_id(self, idusuario: int) -> Optional[Usuario]:
        """Obtiene un usuario por su ID"""
        pass
    
    @abstractmethod
    def actualizar(self, idusuario: int, usuario: Usuario) -> Optional[Usuario]:
        """Actualiza un usuario existente"""
        pass
    
    @abstractmethod
    def eliminar(self, idusuario: int) -> bool:
        """Elimina un usuario"""
        pass

# Puerto (interfaz) del repositorio de Clientes
from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models import Cliente

class RepositorioCliente(ABC):
    """Interfaz del repositorio de clientes siguiendo arquitectura hexagonal"""
    
    @abstractmethod
    def crear(self, cliente: Cliente) -> Cliente:
        """Crea un nuevo cliente"""
        pass
    
    @abstractmethod
    def obtener_todos(self) -> List[Cliente]:
        """Obtiene todos los clientes"""
        pass
    
    @abstractmethod
    def obtener_por_id(self, idcliente: int) -> Optional[Cliente]:
        """Obtiene un cliente por su ID"""
        pass

    @abstractmethod
    def obtener_por_cel(self, cel: str) -> Optional[Cliente]:
        """Obtiene un cliente por número de teléfono"""
        pass
    
    @abstractmethod
    def actualizar(self, idcliente: int, cliente: Cliente) -> Optional[Cliente]:
        """Actualiza un cliente existente"""
        pass
    
    @abstractmethod
    def eliminar(self, idcliente: int) -> bool:
        """Elimina un cliente"""
        pass

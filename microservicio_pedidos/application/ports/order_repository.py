# Puerto (interfaz) del repositorio de Pedidos
from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models import Pedido

class RepositorioPedido(ABC):
    """Interfaz del repositorio de pedidos siguiendo arquitectura hexagonal"""
    
    @abstractmethod
    def crear(self, pedido: Pedido) -> Pedido:
        """Crea un nuevo pedido"""
        pass
    
    @abstractmethod
    def obtener_todos(self) -> List[Pedido]:
        """Obtiene todos los pedidos"""
        pass
    
    @abstractmethod
    def obtener_por_id(self, idpedido: int) -> Optional[Pedido]:
        """Obtiene un pedido por su ID"""
        pass
    
    @abstractmethod
    def actualizar(self, idpedido: int, pedido: Pedido) -> Optional[Pedido]:
        """Actualiza un pedido existente"""
        pass
    
    @abstractmethod
    def eliminar(self, idpedido: int) -> bool:
        """Elimina un pedido"""
        pass

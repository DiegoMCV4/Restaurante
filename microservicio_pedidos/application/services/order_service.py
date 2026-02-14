# Servicio de aplicación para Pedidos
from typing import List, Optional
from domain.models import Pedido
from application.ports.order_repository import RepositorioPedido

class ServicioPedido:
    """Servicio de aplicación que contiene la lógica de negocio de pedidos"""
    
    def __init__(self, repositorio: RepositorioPedido):
        self.repositorio = repositorio
    
    def crear(self, pedido: Pedido) -> Pedido:
        """Registra un nuevo pedido en el sistema"""
        return self.repositorio.crear(pedido)
    
    def obtener_todos(self) -> List[Pedido]:
        """Consulta todos los pedidos registrados"""
        return self.repositorio.obtener_todos()
    
    def obtener_por_id(self, idpedido: int) -> Optional[Pedido]:
        """Consulta la información de un pedido específico"""
        return self.repositorio.obtener_por_id(idpedido)
    
    def actualizar(self, idpedido: int, pedido: Pedido) -> Optional[Pedido]:
        """Modifica un pedido existente"""
        return self.repositorio.actualizar(idpedido, pedido)
    
    def eliminar(self, idpedido: int) -> bool:
        """Elimina un pedido del sistema"""
        return self.repositorio.eliminar(idpedido)

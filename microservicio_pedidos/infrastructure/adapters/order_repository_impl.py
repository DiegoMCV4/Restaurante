# Adaptador de infraestructura - Implementación del repositorio de Pedidos
from typing import List, Optional
from application.ports.order_repository import RepositorioPedido
from domain.models import Pedido

class RepositorioPedidoImpl(RepositorioPedido):
    """Implementación del repositorio de pedidos usando almacenamiento en memoria"""
    
    def __init__(self):
        self.pedidos: List[Pedido] = []
    
    def crear(self, pedido: Pedido) -> Pedido:
        """Crea un nuevo pedido"""
        self.pedidos.append(pedido)
        return pedido
    
    def obtener_todos(self) -> List[Pedido]:
        """Retorna todos los pedidos"""
        return self.pedidos
    
    def obtener_por_id(self, idpedido: int) -> Optional[Pedido]:
        """Busca un pedido por su ID"""
        for pedido in self.pedidos:
            if pedido.idpedido == idpedido:
                return pedido
        return None
    
    def actualizar(self, idpedido: int, pedido: Pedido) -> Optional[Pedido]:
        """Actualiza un pedido existente"""
        for i, p in enumerate(self.pedidos):
            if p.idpedido == idpedido:
                self.pedidos[i] = pedido
                return pedido
        return None
    
    def eliminar(self, idpedido: int) -> bool:
        """Elimina un pedido"""
        for pedido in self.pedidos:
            if pedido.idpedido == idpedido:
                self.pedidos.remove(pedido)
                return True
        return False

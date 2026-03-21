# Puerto: caché de clientes en el microservicio de Pedidos
from abc import ABC, abstractmethod


class ClienteCacheRepositorio(ABC):
    @abstractmethod
    def guardar(self, idcliente: int, nombre: str, cel: str, email: str) -> None:
        """Inserta o actualiza un cliente en la caché local."""
        pass

    @abstractmethod
    def existe(self, idcliente: int) -> bool:
        """Retorna True si el cliente está en la caché."""
        pass

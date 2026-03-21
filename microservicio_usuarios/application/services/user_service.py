# Servicio de aplicación para Clientes
from typing import List, Optional
from domain.models import Cliente
from application.ports.user_repository import RepositorioCliente

class ServicioCliente:
    """Servicio de aplicación que contiene la lógica de negocio de clientes"""
    
    def __init__(self, repositorio: RepositorioCliente):
        self.repositorio = repositorio
    
    def crear(self, cliente: Cliente) -> Cliente:
        """Registra un nuevo cliente en el sistema"""
        return self.repositorio.crear(cliente)
    
    def obtener_todos(self) -> List[Cliente]:
        """Consulta todos los clientes registrados"""
        return self.repositorio.obtener_todos()
    
    def obtener_por_id(self, idcliente: int) -> Optional[Cliente]:
        """Consulta la información de un cliente específico"""
        return self.repositorio.obtener_por_id(idcliente)

    def obtener_por_cel(self, cel: str) -> Optional[Cliente]:
        """Consulta la información de un cliente por teléfono"""
        return self.repositorio.obtener_por_cel(cel)
    
    def actualizar(self, idcliente: int, cliente: Cliente) -> Optional[Cliente]:
        """Modifica los datos de un cliente existente"""
        return self.repositorio.actualizar(idcliente, cliente)
    
    def eliminar(self, idcliente: int) -> bool:
        """Elimina un cliente del sistema"""
        return self.repositorio.eliminar(idcliente)

# Adaptador de infraestructura - Implementación del repositorio de Usuarios
from typing import List, Optional
from application.ports.user_repository import RepositorioUsuario
from domain.models import Usuario

class RepositorioUsuarioImpl(RepositorioUsuario):
    """Implementación del repositorio de usuarios usando almacenamiento en memoria"""
    
    def __init__(self):
        self.usuarios: List[Usuario] = []
    
    def crear(self, usuario: Usuario) -> Usuario:
        """Crea un nuevo usuario"""
        self.usuarios.append(usuario)
        return usuario
    
    def obtener_todos(self) -> List[Usuario]:
        """Retorna todos los usuarios"""
        return self.usuarios
    
    def obtener_por_id(self, idusuario: int) -> Optional[Usuario]:
        """Busca un usuario por su ID"""
        for usuario in self.usuarios:
            if usuario.idusuario == idusuario:
                return usuario
        return None
    
    def actualizar(self, idusuario: int, usuario: Usuario) -> Optional[Usuario]:
        """Actualiza un usuario existente"""
        for i, u in enumerate(self.usuarios):
            if u.idusuario == idusuario:
                self.usuarios[i] = usuario
                return usuario
        return None
    
    def eliminar(self, idusuario: int) -> bool:
        """Elimina un usuario"""
        for usuario in self.usuarios:
            if usuario.idusuario == idusuario:
                self.usuarios.remove(usuario)
                return True
        return False

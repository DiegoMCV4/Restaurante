# Adaptador: caché de clientes almacenada en MySQL (microservicio_pedidos)
import os

from sqlalchemy import create_engine, text

from application.ports.cliente_cache_repository import ClienteCacheRepositorio


class ClienteCacheRepositoryImpl(ClienteCacheRepositorio):
    """Mantiene una tabla clientes_cache en MySQL para validar idcliente."""

    def __init__(self):
        self.database_url = os.getenv(
            "PEDIDOS_DATABASE_URL",
            "mysql+pymysql://root:root@localhost:3306/pedidos_db",
        )
        self.engine = create_engine(self.database_url, future=True)
        self._crear_tabla()

    def _crear_tabla(self) -> None:
        with self.engine.begin() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS clientes_cache (
                    idcliente INT PRIMARY KEY,
                    nombre VARCHAR(120) NOT NULL,
                    cel VARCHAR(30) NOT NULL,
                    email VARCHAR(255) NOT NULL
                )
            """))

    def guardar(self, idcliente: int, nombre: str, cel: str, email: str) -> None:
        query = text("""
            INSERT INTO clientes_cache (idcliente, nombre, cel, email)
            VALUES (:idcliente, :nombre, :cel, :email)
            ON DUPLICATE KEY UPDATE nombre = :nombre, cel = :cel, email = :email
        """)
        with self.engine.begin() as conn:
            conn.execute(query, {
                "idcliente": idcliente,
                "nombre": nombre,
                "cel": cel,
                "email": email,
            })

    def existe(self, idcliente: int) -> bool:
        query = text("SELECT 1 FROM clientes_cache WHERE idcliente = :idcliente")
        with self.engine.connect() as conn:
            row = conn.execute(query, {"idcliente": idcliente}).first()
        return row is not None

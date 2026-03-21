# Adaptador de infraestructura - Implementación del repositorio de Clientes
import os
from typing import List, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from application.ports.user_repository import RepositorioCliente
from domain.models import Cliente

class RepositorioClientePostgres(RepositorioCliente):
    """Implementación del repositorio de clientes en PostgreSQL"""
    
    def __init__(self):
        self.database_url = os.getenv(
            "CLIENTES_DATABASE_URL",
            "postgresql+psycopg2://postgres:postgres@localhost:5432/clientes_db"
        )
        self.engine = create_engine(self.database_url, future=True)
        self._crear_tabla()
    
    def _crear_tabla(self) -> None:
        with self.engine.begin() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS clientes (
                    idcliente INTEGER PRIMARY KEY,
                    nombre VARCHAR(120) NOT NULL,
                    cel VARCHAR(30) NOT NULL,
                    email VARCHAR(255) NOT NULL UNIQUE
                )
            """))
            # Si no hay duplicados históricos, se refuerza unicidad de teléfono en BD.
            duplicated_cel_count = conn.execute(text("""
                SELECT COUNT(*)
                FROM (
                    SELECT cel
                    FROM clientes
                    GROUP BY cel
                    HAVING COUNT(*) > 1
                ) t
            """)).scalar_one()
            if duplicated_cel_count == 0:
                conn.execute(text("""
                    CREATE UNIQUE INDEX IF NOT EXISTS ux_clientes_cel
                    ON clientes (cel)
                """))

    def ping(self) -> bool:
        """Verifica conectividad básica con PostgreSQL."""
        with self.engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    
    def crear(self, cliente: Cliente) -> Cliente:
        """Crea un nuevo cliente"""
        query = text("""
            INSERT INTO clientes (idcliente, nombre, cel, email)
            VALUES (:idcliente, :nombre, :cel, :email)
        """)
        try:
            with self.engine.begin() as conn:
                conn.execute(
                    query,
                    {
                        "idcliente": cliente.idcliente,
                        "nombre": cliente.nombre,
                        "cel": cliente.cel,
                        "email": cliente.email,
                    },
                )
        except IntegrityError as exc:
            raise ValueError("El cliente ya existe o email duplicado") from exc
        return cliente
    
    def obtener_todos(self) -> List[Cliente]:
        """Retorna todos los clientes"""
        query = text("""
            SELECT idcliente, nombre, cel, email
            FROM clientes
            ORDER BY idcliente
        """)
        with self.engine.connect() as conn:
            rows = conn.execute(query).mappings().all()
        return [Cliente(**row) for row in rows]
    
    def obtener_por_id(self, idcliente: int) -> Optional[Cliente]:
        """Busca un cliente por su ID"""
        query = text("""
            SELECT idcliente, nombre, cel, email
            FROM clientes
            WHERE idcliente = :idcliente
        """)
        with self.engine.connect() as conn:
            row = conn.execute(query, {"idcliente": idcliente}).mappings().first()
        return Cliente(**row) if row else None

    def obtener_por_cel(self, cel: str) -> Optional[Cliente]:
        """Busca un cliente por número telefónico"""
        query = text("""
            SELECT idcliente, nombre, cel, email
            FROM clientes
            WHERE cel = :cel
            LIMIT 1
        """)
        with self.engine.connect() as conn:
            row = conn.execute(query, {"cel": cel}).mappings().first()
        return Cliente(**row) if row else None
    
    def actualizar(self, idcliente: int, cliente: Cliente) -> Optional[Cliente]:
        """Actualiza un cliente existente"""
        query = text("""
            UPDATE clientes
            SET nombre = :nombre, cel = :cel, email = :email
            WHERE idcliente = :idcliente
        """)
        try:
            with self.engine.begin() as conn:
                result = conn.execute(
                    query,
                    {
                        "idcliente": idcliente,
                        "nombre": cliente.nombre,
                        "cel": cliente.cel,
                        "email": cliente.email,
                    },
                )
        except IntegrityError as exc:
            raise ValueError("Teléfono o email duplicado") from exc
        if result.rowcount == 0:
            return None
        return Cliente(idcliente=idcliente, nombre=cliente.nombre, cel=cliente.cel, email=cliente.email)

    def eliminar(self, idcliente: int) -> bool:
        """Elimina un cliente"""
        query = text("DELETE FROM clientes WHERE idcliente = :idcliente")
        with self.engine.begin() as conn:
            result = conn.execute(query, {"idcliente": idcliente})
        return result.rowcount > 0

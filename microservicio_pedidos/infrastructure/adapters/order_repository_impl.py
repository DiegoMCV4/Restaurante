# Adaptador de infraestructura - Implementación del repositorio de Pedidos
import os
from typing import List, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from application.ports.order_repository import RepositorioPedido
from domain.models import Pedido

class RepositorioPedidoImpl(RepositorioPedido):
    """Implementación del repositorio de pedidos en MySQL"""
    
    def __init__(self):
        self.database_url = os.getenv(
            "PEDIDOS_DATABASE_URL",
            "mysql+pymysql://root:root@localhost:3306/pedidos_db"
        )
        self.engine = create_engine(self.database_url, future=True)
        self._crear_tabla()
    
    def _crear_tabla(self) -> None:
        with self.engine.begin() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS pedidos (
                    idpedido INT PRIMARY KEY,
                    descripcion TEXT NOT NULL,
                    nombre_pedido VARCHAR(255) NOT NULL,
                    cantidad INT NOT NULL,
                    precio DECIMAL(10,2) NOT NULL,
                    idcliente INT NOT NULL,
                    total DECIMAL(10,2) NOT NULL DEFAULT 0.00
                )
            """))
            # Compatibilidad con tablas creadas en versiones anteriores.
            conn.execute(text("""
                ALTER TABLE pedidos
                MODIFY COLUMN nombre_pedido VARCHAR(255) NOT NULL
            """))
            total_exists = conn.execute(text("""
                SELECT COUNT(*)
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE()
                  AND TABLE_NAME = 'pedidos'
                  AND COLUMN_NAME = 'total'
            """)).scalar_one()
            if not total_exists:
                conn.execute(text("""
                    ALTER TABLE pedidos
                    ADD COLUMN total DECIMAL(10,2) NOT NULL DEFAULT 0.00
                """))
            conn.execute(text("""
                UPDATE pedidos
                SET total = ROUND(cantidad * precio, 2)
                WHERE total = 0.00
            """))

    @staticmethod
    def _calcular_total(cantidad: int, precio: float) -> float:
        return round(cantidad * precio, 2)

    def ping(self) -> bool:
        """Verifica conectividad básica con MySQL."""
        with self.engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    
    def crear(self, pedido: Pedido) -> Pedido:
        """Crea un nuevo pedido"""
        total = self._calcular_total(pedido.cantidad, pedido.precio)
        query = text("""
            INSERT INTO pedidos (idpedido, descripcion, nombre_pedido, cantidad, precio, idcliente, total)
            VALUES (:idpedido, :descripcion, :nombre_pedido, :cantidad, :precio, :idcliente, :total)
        """)
        try:
            with self.engine.begin() as conn:
                conn.execute(
                    query,
                    {
                        "idpedido": pedido.idpedido,
                        "descripcion": pedido.descripcion,
                        "nombre_pedido": pedido.nombre_pedido,
                        "cantidad": pedido.cantidad,
                        "precio": pedido.precio,
                        "idcliente": pedido.idcliente,
                        "total": total,
                    },
                )
        except IntegrityError as exc:
            raise ValueError("El pedido ya existe") from exc
        pedido.total = total
        return pedido
    
    def obtener_todos(self) -> List[Pedido]:
        """Retorna todos los pedidos"""
        query = text("""
            SELECT idpedido, descripcion, nombre_pedido, cantidad, precio, idcliente, total
            FROM pedidos
            ORDER BY idpedido
        """)
        with self.engine.connect() as conn:
            rows = conn.execute(query).mappings().all()
        return [
            Pedido(**{**row, "precio": float(row["precio"]), "total": float(row["total"])})
            for row in rows
        ]
    
    def obtener_por_id(self, idpedido: int) -> Optional[Pedido]:
        """Busca un pedido por su ID"""
        query = text("""
            SELECT idpedido, descripcion, nombre_pedido, cantidad, precio, idcliente, total
            FROM pedidos
            WHERE idpedido = :idpedido
        """)
        with self.engine.connect() as conn:
            row = conn.execute(query, {"idpedido": idpedido}).mappings().first()
        if not row:
            return None
        return Pedido(**{**row, "precio": float(row["precio"]), "total": float(row["total"])})
    
    def actualizar(self, idpedido: int, pedido: Pedido) -> Optional[Pedido]:
        """Actualiza un pedido existente"""
        total = self._calcular_total(pedido.cantidad, pedido.precio)
        query = text("""
            UPDATE pedidos
            SET descripcion = :descripcion,
                nombre_pedido = :nombre_pedido,
                cantidad = :cantidad,
                precio = :precio,
                idcliente = :idcliente,
                total = :total
            WHERE idpedido = :idpedido
        """)
        with self.engine.begin() as conn:
            result = conn.execute(
                query,
                {
                    "idpedido": idpedido,
                    "descripcion": pedido.descripcion,
                    "nombre_pedido": pedido.nombre_pedido,
                    "cantidad": pedido.cantidad,
                    "precio": pedido.precio,
                    "idcliente": pedido.idcliente,
                    "total": total,
                },
            )
        if result.rowcount == 0:
            return None
        return Pedido(
            idpedido=idpedido,
            descripcion=pedido.descripcion,
            nombre_pedido=pedido.nombre_pedido,
            cantidad=pedido.cantidad,
            precio=pedido.precio,
            idcliente=pedido.idcliente,
            total=total,
        )

    def eliminar(self, idpedido: int) -> bool:
        """Elimina un pedido"""
        query = text("DELETE FROM pedidos WHERE idpedido = :idpedido")
        with self.engine.begin() as conn:
            result = conn.execute(query, {"idpedido": idpedido})
        return result.rowcount > 0

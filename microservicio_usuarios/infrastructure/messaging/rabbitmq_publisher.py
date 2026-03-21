import json
import os
from typing import Any

import pika
from pika.exceptions import AMQPConnectionError

# Exchange fanout: todos los suscriptores reciben cada evento de cliente
CLIENTES_EXCHANGE = "clientes.eventos"


class RabbitMQClientePublisher:
    """Publicador de eventos de clientes hacia RabbitMQ."""

    def __init__(self) -> None:
        self.host = os.getenv("RABBITMQ_HOST", "localhost")
        self.port = int(os.getenv("RABBITMQ_PORT", "5672"))
        self.user = os.getenv("RABBITMQ_USER", "guest")
        self.password = os.getenv("RABBITMQ_PASSWORD", "guest")

    def _connection_parameters(self) -> pika.ConnectionParameters:
        credentials = pika.PlainCredentials(self.user, self.password)
        return pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            credentials=credentials,
            heartbeat=60,
            blocked_connection_timeout=30,
        )

    def ping(self) -> bool:
        """Verifica conectividad básica con RabbitMQ."""
        try:
            connection = pika.BlockingConnection(self._connection_parameters())
            connection.close()
            return True
        except AMQPConnectionError as exc:
            raise RuntimeError("No se pudo conectar a RabbitMQ") from exc

    def publicar_cliente_creado(self, payload: dict[str, Any]) -> None:
        """Publica un evento de creación de cliente en el exchange fanout."""
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        try:
            connection = pika.BlockingConnection(self._connection_parameters())
            channel = connection.channel()
            channel.exchange_declare(
                exchange=CLIENTES_EXCHANGE, exchange_type="fanout", durable=True
            )
            channel.basic_publish(
                exchange=CLIENTES_EXCHANGE,
                routing_key="",
                body=body,
                properties=pika.BasicProperties(delivery_mode=2),
            )
            connection.close()
        except AMQPConnectionError as exc:
            raise RuntimeError("No se pudo publicar el cliente en RabbitMQ") from exc

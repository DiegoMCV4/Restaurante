import json
import os
from typing import Any

import pika
from pika.exceptions import AMQPConnectionError


class RabbitMQPedidoPublisher:
    """Publicador de eventos de pedidos hacia RabbitMQ."""

    def __init__(self) -> None:
        self.host = os.getenv("RABBITMQ_HOST", "localhost")
        self.port = int(os.getenv("RABBITMQ_PORT", "5672"))
        self.user = os.getenv("RABBITMQ_USER", "guest")
        self.password = os.getenv("RABBITMQ_PASSWORD", "guest")
        self.queue = os.getenv("PEDIDOS_QUEUE", "pedidos.creados")

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

    def publicar_pedido_creado(self, payload: dict[str, Any]) -> None:
        """Publica un evento de creación de pedido en la cola durable."""
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        try:
            connection = pika.BlockingConnection(self._connection_parameters())
            channel = connection.channel()
            channel.queue_declare(queue=self.queue, durable=True)
            channel.basic_publish(
                exchange="",
                routing_key=self.queue,
                body=body,
                properties=pika.BasicProperties(delivery_mode=2),
            )
            connection.close()
        except AMQPConnectionError as exc:
            raise RuntimeError("No se pudo publicar el pedido en RabbitMQ") from exc

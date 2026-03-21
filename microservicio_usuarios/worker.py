import json
import os
import time

import pika
from pika.exceptions import AMQPConnectionError

from domain.models import Cliente
from infrastructure.adapters.user_repository_impl import RepositorioClientePostgres

# Exchange fanout compartido con el microservicio de Pedidos
CLIENTES_EXCHANGE = "clientes.eventos"


def get_connection_parameters() -> pika.ConnectionParameters:
    host = os.getenv("RABBITMQ_HOST", "localhost")
    port = int(os.getenv("RABBITMQ_PORT", "5672"))
    user = os.getenv("RABBITMQ_USER", "guest")
    password = os.getenv("RABBITMQ_PASSWORD", "guest")
    credentials = pika.PlainCredentials(user, password)
    return pika.ConnectionParameters(
        host=host,
        port=port,
        credentials=credentials,
        heartbeat=60,
        blocked_connection_timeout=30,
    )


def run_worker() -> None:
    queue = os.getenv("CLIENTES_QUEUE", "clientes.creados")
    repo = RepositorioClientePostgres()

    while True:
        connection = None
        try:
            connection = pika.BlockingConnection(get_connection_parameters())
            channel = connection.channel()
            # Declarar exchange fanout y enlazar la cola de postgres
            channel.exchange_declare(
                exchange=CLIENTES_EXCHANGE, exchange_type="fanout", durable=True
            )
            channel.queue_declare(queue=queue, durable=True)
            channel.queue_bind(exchange=CLIENTES_EXCHANGE, queue=queue)
            channel.basic_qos(prefetch_count=1)

            def callback(ch, method, properties, body):
                try:
                    data = json.loads(body.decode("utf-8"))
                    cliente = Cliente.model_validate(data)
                    try:
                        repo.crear(cliente)
                    except ValueError:
                        # Mensaje duplicado: se confirma para evitar reintentos infinitos.
                        ch.basic_ack(delivery_tag=method.delivery_tag)
                        return
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                except Exception:
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

            channel.basic_consume(queue=queue, on_message_callback=callback)
            print(f"[worker-clientes] Escuchando cola {queue}")
            channel.start_consuming()
        except AMQPConnectionError:
            print("[worker-clientes] RabbitMQ no disponible, reintentando en 3s...")
            time.sleep(3)
        finally:
            if connection and connection.is_open:
                connection.close()


if __name__ == "__main__":
    run_worker()

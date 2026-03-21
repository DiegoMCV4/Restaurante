import json
import os
import time
import threading

import pika
from pika.exceptions import AMQPConnectionError

from domain.models import Pedido
from infrastructure.adapters.order_repository_impl import RepositorioPedidoImpl
from infrastructure.adapters.cliente_cache_repository_impl import ClienteCacheRepositoryImpl

# Exchange fanout declarado por el microservicio de Clientes
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
    queue = os.getenv("PEDIDOS_QUEUE", "pedidos.creados")
    repo = RepositorioPedidoImpl()

    while True:
        connection = None
        try:
            connection = pika.BlockingConnection(get_connection_parameters())
            channel = connection.channel()
            channel.queue_declare(queue=queue, durable=True)
            channel.basic_qos(prefetch_count=1)

            def callback(ch, method, properties, body):
                try:
                    data = json.loads(body.decode("utf-8"))
                    pedido = Pedido.model_validate(data)
                    try:
                        repo.crear(pedido)
                    except ValueError:
                        # Mensaje duplicado: se confirma para evitar reintentos infinitos.
                        ch.basic_ack(delivery_tag=method.delivery_tag)
                        return
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                except Exception:
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

            channel.basic_consume(queue=queue, on_message_callback=callback)
            print(f"[worker-pedidos] Escuchando cola {queue}")
            channel.start_consuming()
        except AMQPConnectionError:
            print("[worker-pedidos] RabbitMQ no disponible, reintentando en 3s...")
            time.sleep(3)
        finally:
            if connection and connection.is_open:
                connection.close()


def run_clientes_cache_worker() -> None:
    """Consume eventos de clientes desde el exchange fanout y los cachea en MySQL."""
    queue = os.getenv("CLIENTES_CACHE_QUEUE", "clientes.cache.pedidos")
    cache_repo = ClienteCacheRepositoryImpl()

    while True:
        connection = None
        try:
            connection = pika.BlockingConnection(get_connection_parameters())
            channel = connection.channel()
            channel.exchange_declare(
                exchange=CLIENTES_EXCHANGE, exchange_type="fanout", durable=True
            )
            channel.queue_declare(queue=queue, durable=True)
            channel.queue_bind(exchange=CLIENTES_EXCHANGE, queue=queue)
            channel.basic_qos(prefetch_count=1)

            def callback(ch, method, properties, body):
                try:
                    data = json.loads(body.decode("utf-8"))
                    cache_repo.guardar(
                        idcliente=data["idcliente"],
                        nombre=data["nombre"],
                        cel=data["cel"],
                        email=data["email"],
                    )
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                except Exception:
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

            channel.basic_consume(queue=queue, on_message_callback=callback)
            print(f"[worker-cache] Escuchando cola {queue}")
            channel.start_consuming()
        except AMQPConnectionError:
            print("[worker-cache] RabbitMQ no disponible, reintentando en 3s...")
            time.sleep(3)
        finally:
            if connection and connection.is_open:
                connection.close()


if __name__ == "__main__":
    # Hilo daemon: sincroniza clientes desde RabbitMQ → MySQL cache
    t = threading.Thread(target=run_clientes_cache_worker, daemon=True)
    t.start()
    # Hilo principal: persiste pedidos desde RabbitMQ → MySQL
    run_worker()

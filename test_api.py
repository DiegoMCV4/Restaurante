import requests
import time

BASE_URL_CLIENTES = "http://localhost:8001"
BASE_URL_ORDERS = "http://localhost:8002"

def print_separator(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

# ============= CLIENTES =============

print_separator("1. CREAR CLIENTES")
clientes = [
    {"idcliente": 1, "nombre": "Juan Pérez", "cel": "5551001", "email": "juan@example.com"},
    {"idcliente": 2, "nombre": "María García", "cel": "5551002", "email": "maria@example.com"},
    {"idcliente": 3, "nombre": "Carlos López", "cel": "5551003", "email": "carlos@example.com"}
]

for cliente in clientes:
    response = requests.post(f"{BASE_URL_CLIENTES}/clientes", json=cliente)
    print(f"✅ Cliente creado: {response.json()}")

# Esperar a que worker_clientes persista en Postgres y worker_cache en MySQL
print("⏳ Esperando sincronización de clientes en caché...")
time.sleep(3)

print_separator("2. OBTENER TODOS LOS CLIENTES")
response = requests.get(f"{BASE_URL_CLIENTES}/clientes")
print(f"📋 Total de clientes: {len(response.json())}")
for cliente in response.json():
    print(f"  - {cliente['nombre']} ({cliente['email']})")

print_separator("3. ACTUALIZAR CLIENTE")
cliente_actualizado = {
    "idcliente": 1,
    "nombre": "Juan Carlos Pérez Actualizado",
    "cel": "5552001",
    "email": "juancarlos@example.com"
}
response = requests.put(f"{BASE_URL_CLIENTES}/clientes/1", json=cliente_actualizado)
print(f"✏️ Cliente actualizado: {response.json()}")

# ============= PEDIDOS =============

print_separator("4. CREAR PEDIDOS")
pedidos = [
    {
        "idpedido": 1,
        "descripcion": "Pizza Margherita, Ensalada César, 2 Cervezas",
        "nombre_pedido": "Pizza",
        "cantidad": 2,
        "precio": 45.99,
        "idcliente": 1
    },
    {
        "idpedido": 2,
        "descripcion": "Hamburguesa, Papas fritas, Refresco",
        "nombre_pedido": "Burger",
        "cantidad": 1,
        "precio": 15.50,
        "idcliente": 2
    },
    {
        "idpedido": 3,
        "descripcion": "Espaguetis a la Carbonara, Agua",
        "nombre_pedido": "Pasta",
        "cantidad": 1,
        "precio": 18.75,
        "idcliente": 3
    }
]

for pedido in pedidos:
    response = requests.post(f"{BASE_URL_ORDERS}/pedidos", json=pedido)
    print(f"✅ Pedido creado: ID {response.json()['idpedido']}")

# Persistencia asíncrona: se espera un instante a que el worker consuma la cola.
time.sleep(2)

print_separator("5. OBTENER TODOS LOS PEDIDOS")
response = requests.get(f"{BASE_URL_ORDERS}/pedidos")
print(f"📋 Total de pedidos: {len(response.json())}")
for order in response.json():
    print(f"  - Pedido #{order['idpedido']}: {order['descripcion']} - Cliente: {order['idcliente']}")

print_separator("6. OBTENER PEDIDO POR ID")
response = requests.get(f"{BASE_URL_ORDERS}/pedidos/1")
pedido = response.json()
print(f"ID: {pedido['idpedido']}")
print(f"Cliente: {pedido['idcliente']}")
print(f"Descripción: {pedido['descripcion']}")
print(f"Nombre pedido: {pedido['nombre_pedido']}")
print(f"Cantidad: {pedido['cantidad']}")
print(f"Precio: ${pedido['precio']}")

print_separator("7. ACTUALIZAR PEDIDO")
pedido_actualizado = {
    "idpedido": 1,
    "descripcion": "Pizza Margherita, Ensalada César, 2 Cervezas",
    "nombre_pedido": "Pizza",
    "cantidad": 3,
    "precio": 45.99,
    "idcliente": 1
}
response = requests.put(f"{BASE_URL_ORDERS}/pedidos/1", json=pedido_actualizado)
print(f"✏️ Pedido actualizado - Nueva cantidad: {response.json()['cantidad']}")

print_separator("8. ELIMINAR PEDIDO")
response = requests.delete(f"{BASE_URL_ORDERS}/pedidos/2")
print(f"🗑️ Pedido eliminado: {response.json()}")

print_separator("9. VERIFICAR PEDIDOS RESTANTES")
response = requests.get(f"{BASE_URL_ORDERS}/pedidos")
print(f"📋 Total de pedidos después de eliminación: {len(response.json())}")

print_separator("10. ELIMINAR CLIENTE")
response = requests.delete(f"{BASE_URL_CLIENTES}/clientes/3")
print(f"🗑️ Cliente eliminado: {response.json()}")

print_separator("RESUMEN FINAL")
clientes_response = requests.get(f"{BASE_URL_CLIENTES}/clientes")
orders_response = requests.get(f"{BASE_URL_ORDERS}/pedidos")
print(f"✅ Total de clientes: {len(clientes_response.json())}")
print(f"✅ Total de pedidos: {len(orders_response.json())}")
print("\n¡Pruebas completadas correctamente!")

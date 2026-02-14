import requests
import json

BASE_URL_USERS = "http://localhost:8001"
BASE_URL_ORDERS = "http://localhost:8002"

def print_separator(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

# ============= USUARIOS =============

print_separator("1. CREAR USUARIOS")
usuarios = [
    {"idusuario": 1, "nombre": "Juan Pérez", "email": "juan@example.com"},
    {"idusuario": 2, "nombre": "María García", "email": "maria@example.com"},
    {"idusuario": 3, "nombre": "Carlos López", "email": "carlos@example.com"}
]

for usuario in usuarios:
    response = requests.post(f"{BASE_URL_USERS}/users", json=usuario)
    print(f"✅ Usuario creado: {response.json()}")

print_separator("2. OBTENER TODOS LOS USUARIOS")
response = requests.get(f"{BASE_URL_USERS}/users")
print(f"📋 Total de usuarios: {len(response.json())}")
for user in response.json():
    print(f"  - {user['nombre']} ({user['email']})")

print_separator("3. ACTUALIZAR USUARIO")
usuario_actualizado = {
    "idusuario": 1,
    "nombre": "Juan Carlos Pérez Actualizado",
    "email": "juancarlos@example.com"
}
response = requests.put(f"{BASE_URL_USERS}/users/1", json=usuario_actualizado)
print(f"✏️ Usuario actualizado: {response.json()}")

# ============= PEDIDOS =============

print_separator("4. CREAR PEDIDOS")
pedidos = [
    {
        "id_pedido": 1,
        "id_usuario": 1,
        "descripcion": "Pizza Margherita, Ensalada César, 2 Cervezas",
        "estado": "pendiente",
        "fecha": "2026-02-13",
        "total": 45.99
    },
    {
        "id_pedido": 2,
        "id_usuario": 2,
        "descripcion": "Hamburguesa, Papas fritas, Refresco",
        "estado": "en preparación",
        "fecha": "2026-02-13",
        "total": 15.50
    },
    {
        "id_pedido": 3,
        "id_usuario": 3,
        "descripcion": "Espaguetis a la Carbonara, Agua",
        "estado": "entregado",
        "fecha": "2026-02-13",
        "total": 18.75
    }
]

for pedido in pedidos:
    response = requests.post(f"{BASE_URL_ORDERS}/orders", json=pedido)
    print(f"✅ Pedido creado: ID {response.json()['id_pedido']}")

print_separator("5. OBTENER TODOS LOS PEDIDOS")
response = requests.get(f"{BASE_URL_ORDERS}/orders")
print(f"📋 Total de pedidos: {len(response.json())}")
for order in response.json():
    print(f"  - Pedido #{order['id_pedido']}: {order['descripcion']} - Estado: {order['estado']}")

print_separator("6. OBTENER PEDIDO POR ID")
response = requests.get(f"{BASE_URL_ORDERS}/orders/1")
pedido = response.json()
print(f"ID: {pedido['id_pedido']}")
print(f"Usuario: {pedido['id_usuario']}")
print(f"Descripción: {pedido['descripcion']}")
print(f"Estado: {pedido['estado']}")
print(f"Fecha: {pedido['fecha']}")
print(f"Total: ${pedido['total']}")

print_separator("7. ACTUALIZAR PEDIDO (cambiar estado)")
pedido_actualizado = {
    "id_pedido": 1,
    "id_usuario": 1,
    "descripcion": "Pizza Margherita, Ensalada César, 2 Cervezas",
    "estado": "entregado",
    "fecha": "2026-02-13",
    "total": 45.99
}
response = requests.put(f"{BASE_URL_ORDERS}/orders/1", json=pedido_actualizado)
print(f"✏️ Pedido actualizado - Nuevo estado: {response.json()['estado']}")

print_separator("8. ELIMINAR PEDIDO")
response = requests.delete(f"{BASE_URL_ORDERS}/orders/2")
print(f"🗑️ Pedido eliminado: {response.json()}")

print_separator("9. VERIFICAR PEDIDOS RESTANTES")
response = requests.get(f"{BASE_URL_ORDERS}/orders")
print(f"📋 Total de pedidos después de eliminación: {len(response.json())}")

print_separator("10. ELIMINAR USUARIO")
response = requests.delete(f"{BASE_URL_USERS}/users/3")
print(f"🗑️ Usuario eliminado: {response.json()}")

print_separator("RESUMEN FINAL")
users_response = requests.get(f"{BASE_URL_USERS}/users")
orders_response = requests.get(f"{BASE_URL_ORDERS}/orders")
print(f"✅ Total de usuarios: {len(users_response.json())}")
print(f"✅ Total de pedidos: {len(orders_response.json())}")
print("\n¡Pruebas completadas correctamente!")

# Restaurante Microservices

Proyecto de ejemplo con arquitectura hexagonal y comunicacion asincrona entre microservicios usando RabbitMQ.

Incluye:
- Microservicio de clientes (FastAPI + PostgreSQL)
- Microservicio de pedidos (FastAPI + MySQL)
- Workers para persistencia asincrona
- Cache de clientes en pedidos para validar `idcliente`

## 1. Arquitectura

Servicios principales:
- `microservicio_clientes` expone API REST en `8001`
- `microservicio_pedidos` expone API REST en `8002`
- `worker_clientes` consume eventos de clientes y persiste en PostgreSQL
- `worker_pedidos` consume eventos de pedidos y persiste en MySQL
- `worker_pedidos` tambien consume eventos fanout de clientes para cache local en MySQL

Infraestructura:
- PostgreSQL (`clientes_db`) en `5432`
- MySQL (`pedidos_db`) en `3307` (host) -> `3306` (contenedor)
- RabbitMQ en `5672` y panel en `15672`

Flujo resumido:
1. API Clientes recibe `POST /clientes` y publica evento en exchange `clientes.eventos`.
2. Worker de clientes consume y guarda en PostgreSQL.
3. Worker de pedidos se suscribe al exchange fanout y actualiza `clientes_cache` en MySQL.
4. API Pedidos valida `idcliente` contra `clientes_cache`.
5. API Pedidos recibe `POST /pedidos`, publica a cola `pedidos.creados`.
6. Worker de pedidos consume y persiste en tabla `pedidos`.

## 2. Requisitos

### Opcion recomendada: Docker
- Docker Desktop 4.x+
- Docker Compose v2+

### Opcion local (sin Docker)
- Python 3.12+
- PostgreSQL 16+
- MySQL 8+
- RabbitMQ 3.13+

## 3. Levantar todo rapido con Docker (recomendado)

Desde la raiz del proyecto:

```bash
docker compose up --build -d
```

Ver estado:

```bash
docker compose ps
```

Ver logs en vivo:

```bash
docker compose logs -f
```

Detener y limpiar contenedores (sin borrar volumenes):

```bash
docker compose down
```

Detener y limpiar todo incluyendo volumenes (reset total de datos):

```bash
docker compose down -v
```

## 4. Verificar que esta funcionando

Health checks:

```bash
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8001/clientes/health/db
curl http://localhost:8001/clientes/health/broker
curl http://localhost:8002/pedidos/health/db
curl http://localhost:8002/pedidos/health/broker
```

Swagger:
- http://localhost:8001/docs
- http://localhost:8002/docs

RabbitMQ UI:
- http://localhost:15672
- user: `guest`
- password: `guest`

## 5. Probar flujo completo end-to-end

El repositorio trae un script de prueba:

```bash
python test_api.py
```

Este script:
- crea clientes
- espera sincronizacion asincrona
- crea pedidos
- lista, actualiza y elimina registros

Si los servicios estan arriba, debe terminar con:
- `Pruebas completadas correctamente`

## 6. Crear y ejecutar desde cero sin Docker

Usa esta seccion si quieres correr todos los componentes en tu maquina local.

### 6.1 Clonar e instalar dependencias Python

```bash
git clone <URL_DEL_REPO>
cd restaurante
python -m venv .venv
```

Activar entorno:

- PowerShell (Windows):

```powershell
.\.venv\Scripts\Activate.ps1
```

- Bash (Linux/macOS):

```bash
source .venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

### 6.2 Levantar infraestructura local

Debes tener estos servicios locales y accesibles:
- PostgreSQL en `localhost:5432`
- MySQL en `localhost:3306`
- RabbitMQ en `localhost:5672`

Crear bases:
- `clientes_db` en PostgreSQL
- `pedidos_db` en MySQL

### 6.3 Variables de entorno

Clientes:

```bash
CLIENTES_DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/clientes_db
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest
CLIENTES_QUEUE=clientes.creados
```

Pedidos:

```bash
PEDIDOS_DATABASE_URL=mysql+pymysql://root:root@localhost:3306/pedidos_db
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest
PEDIDOS_QUEUE=pedidos.creados
CLIENTES_CACHE_QUEUE=clientes.cache.pedidos
```

### 6.4 Arranque local en 4 terminales

Terminal 1 (API clientes):

```bash
cd microservicio_usuarios
python main.py
```

Terminal 2 (worker clientes):

```bash
cd microservicio_usuarios
python worker.py
```

Terminal 3 (API pedidos):

```bash
cd microservicio_pedidos
python main.py
```

Terminal 4 (worker pedidos + cache de clientes):

```bash
cd microservicio_pedidos
python worker.py
```

Luego, desde la raiz:

```bash
python test_api.py
```

## 7. Endpoints principales

Clientes (`http://localhost:8001`):
- `POST /clientes` (encola)
- `GET /clientes`
- `GET /clientes/{idcliente}`
- `PUT /clientes/{idcliente}`
- `DELETE /clientes/{idcliente}`

Pedidos (`http://localhost:8002`):
- `POST /pedidos` (encola, valida cliente en cache)
- `GET /pedidos`
- `GET /pedidos/{idpedido}`
- `PUT /pedidos/{idpedido}`
- `DELETE /pedidos/{idpedido}`

## 8. Problemas comunes

### Error 422 al crear pedido
Motivo: `idcliente` no existe en `clientes_cache` aun.

Solucion:
1. Crea primero el cliente en `POST /clientes`.
2. Espera unos segundos a la sincronizacion asincrona.
3. Reintenta el `POST /pedidos`.

### Error de conexion a RabbitMQ o DB
Verifica:
1. Contenedores arriba (`docker compose ps`).
2. Variables de entorno correctas.
3. Puertos libres (`5432`, `3307`, `5672`, `8001`, `8002`, `15672`).

### Cambiaste modelos/tablas y hay estado viejo
Haz reset total:

```bash
docker compose down -v
docker compose up --build -d
```

## 9. Estructura del proyecto

```text
microservicio_usuarios/
  application/
  domain/
  infrastructure/
  main.py
  worker.py

microservicio_pedidos/
  application/
  domain/
  infrastructure/
  main.py
  worker.py

docker-compose.yml
requirements.txt
test_api.py
postman_collection.json
```

## 10. Coleccion Postman

Puedes importar `postman_collection.json` para probar endpoints manualmente.

## 11. Notas de implementacion

- Las tablas se crean automaticamente al iniciar los repositorios.
- La persistencia de `POST /clientes` y `POST /pedidos` es asincrona.
- El campo `total` del pedido se recalcula como `cantidad * precio`.

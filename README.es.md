# MQTT to Corsight Adapter

![Python](https://img.shields.io/badge/python-3.9+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Status](https://img.shields.io/badge/status-active-success.svg?style=for-the-badge)

Este proyecto es un adaptador que recibe eventos de detección facial vía MQTT y los envía a la API de Corsight (Fortify). También incluye un modo de simulación para pruebas sin conexión MQTT activa.

[English Version](README.md)

## Configuración

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# Corsight Configuration
CORSIGHT_API_URL=https://api-corsight.ejemplo.com
CORSIGHT_USER=tu_usuario
CORSIGHT_PASS=tu_contraseña

# MQTT Configuration (Ignorado en modo simulación)
MQTT_BROKER=localhost
MQTT_PORT=1883
MQTT_TOPIC=face/detection
```

## Despliegue

Utiliza el script `deploy.sh` para construir y correr el contenedor Docker.

### Modo Producción (MQTT Activo)

```bash
./deploy.sh
```

### Modo Simulación (HTTP Endpoint Activo)

En este modo, el listener MQTT se desactiva y se habilita un endpoint HTTP `/simulate` para recibir pruebas.

```bash
./deploy.sh --sim
```

> **Nota**: El contenedor usa `network="host"`, por lo que escuchará en el puerto 8000 de tu máquina (o el configurado).

## Pruebas y Simulación Manual

Se incluyen herramientas para probar la integración fácilmente.

### 1. Script de Prueba Automatizado (`run_test.sh`)

Este script ejecuta una prueba completa enviando una petición al contenedor corriendo en modo simulación. Por defecto usa una imagen de prueba generada automáticamente (`tests/fixtures/face.jpg`).

**Uso Básico:**

```bash
./run_test.sh
```

**Uso Avanzado (Personalizar Datos):**
Puedes anular cualquier dato de la persona detectada:

```bash
./run_test.sh --name "Cualquier Persona" --rut "00.000.000-0" --blacklist false --image /ruta/foto.jpg
```

| Argumento | Descripción | Valor por defecto |
|-----------|-------------|-------------------|
| `--image` | Ruta a la imagen (jpg/png) | `tests/fixtures/face.jpg` |
| `--name` | Nombre de la persona | "Test Person" |
| `--rut` | RUT de la persona | "00.000.000-0" |
| `--blacklist`| Es lista negra (`true`/`false`) | `true` |
| `--url` | URL del endpoint de simulación | `http://localhost:8000/simulate` |

## Estructura del Proyecto

```
.
├── deploy.sh               # Script de despliegue Docker
├── run_test.sh             # Script de pruebas automatizadas
├── Dockerfile              # Definición de la imagen Docker
├── requirements.txt        # Dependencias Python
├── README.md               # Documentación del proyecto
├── .env                    # Variables de entorno (no incluido en git)
├── scripts/
│   └── generate_test_image.py  # Utilidad para generar imágenes de prueba
├── src/
│   ├── main.py             # Punto de entrada de la aplicación
│   ├── application/        # Lógica de negocio
│   │   └── use_cases.py    # Casos de uso (ej: Procesar Detección)
│   ├── domain/             # Definiciones de dominio
│   │   └── schemas.py      # Modelos Pydantic
│   ├── infrastructure/     # Implementaciones externas
│   │   ├── config.py       # Configuración global
│   │   ├── corsight.py     # Cliente API Corsight
│   │   ├── mqtt.py         # Cliente MQTT
│   │   └── mock_repository.py # Repositorio simulado
│   └── scripts/            # Scripts internos
│       └── manual_trigger.py # Lógica del trigger manual
└── tests/
    └── fixtures/
        └── face.jpg        # Imagen de prueba por defecto
```

## API Endpoints Reference

### Endpoints Internos (App)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET`  | `/`      | Health check. Retorna estado y entorno. |
| `POST` | `/simulate` | Trigger manual. Recibe payload MQTT-like y procesa la detección. |

### Endpoints Externos (Fortify/Corsight)

Estos son los endpoints que la aplicación consume internamente.

| Servicio | Método | Endpoint | Descripción |
|----------|--------|----------|-------------|
| Auth     | `POST` | `/users_service/auth/login/` | Autenticación. Retorna `token` o `access_token`. |
| POI      | `POST` | `/poi_service/poi_db/poi/`   | Base de datos de POIs. Crea un nuevo sujeto con foto y metadatos. |

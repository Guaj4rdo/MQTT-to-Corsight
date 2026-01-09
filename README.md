# MQTT to Corsight Adapter

![Python](https://img.shields.io/badge/python-3.9+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Status](https://img.shields.io/badge/status-active-success.svg?style=for-the-badge)

This project is an adapter that receives face detection events via MQTT and forwards them to the Corsight API (Fortify). It also includes a simulation mode for testing without an active MQTT connection.

[Ver en Español](README.es.md)

## Configuration

Create a `.env` file in the project root with the following variables:

```env
# Corsight Configuration
CORSIGHT_API_URL=https://172.21.196.136
CORSIGHT_USER=admin
CORSIGHT_PASS=admin

# MQTT Configuration (Ignored in simulation mode)
MQTT_BROKER=127.0.0.1
MQTT_PORT=1883
MQTT_TOPIC=face/detection
```

## Deployment

Use the `deploy.sh` script to build and run the Docker container.

### Production Mode (MQTT Enabled)

```bash
./deploy.sh
```

### Simulation Mode (HTTP Endpoint Enabled)

In this mode, the MQTT listener is disabled and an HTTP `/simulate` endpoint is enabled to receive test requests.

```bash
./deploy.sh --sim
```

> **Note**: The container uses `network="host"`, so it will listen on port 8000 of your machine (or whichever is configured).

## Testing and Manual Simulation

Tools are included to easily test the integration.

### 1. Automated Test Script (`run_test.sh`)

This script executes a full test by sending a request to the container running in simulation mode. By default, it uses an automatically generated test image (`tests/fixtures/face.jpg`).

**Basic Usage:**

```bash
./run_test.sh
```

**Advanced Usage (Customize Data):**
You can override any data of the detected person:

```bash
./run_test.sh --name "John Doe" --rut "11.222.333-4" --blacklist false --image /path/to/my_photo.jpg
```

| Argument | Description | Default Value |
|----------|-------------|---------------|
| `--image` | Path to image (jpg/png) | `tests/fixtures/face.jpg` |
| `--name` | Person name | "Test Person" |
| `--rut` | Person RUT (ID) | "12.345.678-0" |
| `--blacklist`| Is blacklisted (`true`/`false`) | `true` |
| `--url` | Simulation endpoint URL | `http://localhost:8000/simulate` |

## Project Structure

```
.
├── deploy.sh               # Docker deployment script
├── run_test.sh             # Automated testing script
├── Dockerfile              # Docker image definition
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation (English)
├── README.es.md            # Project documentation (Spanish)
├── .env                    # Environment variables (not in git)
├── scripts/
│   └── generate_test_image.py  # Utility to generate test images
├── src/
│   ├── main.py             # Application entry point
│   ├── application/        # Business logic
│   │   └── use_cases.py    # Use cases (e.g., Process Detection)
│   ├── domain/             # Domain definitions
│   │   └── schemas.py      # Pydantic models
│   ├── infrastructure/     # External implementations
│   │   ├── config.py       # Global configuration
│   │   ├── corsight.py     # Corsight API Client
│   │   ├── mqtt.py         # MQTT Client
│   │   └── mock_repository.py # Mock repository
│   └── scripts/            # Internal scripts
│       └── manual_trigger.py # Manual trigger logic
└── tests/
    └── fixtures/
        └── face.jpg        # Default test image
```

## API Endpoints Reference

### Internal Endpoints (App)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/`      | Health check. Returns status and environment. |
| `POST` | `/simulate` | Manual trigger. Receives MQTT-like payload and processes detection. |

### External Endpoints (Fortify/Corsight)

These are the endpoints the application consumes internally.

| Service | Method | Endpoint | Description |
|---------|--------|----------|-------------|
| Auth    | `POST` | `/users_service/auth/login/` | Authentication. Returns `token` or `access_token`. |
| POI     | `POST` | `/poi_service/poi_db/poi/`   | POI Database. Creates a new subject with photo and metadata. |

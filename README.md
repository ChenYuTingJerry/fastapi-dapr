# Dapr Order Payment PoC

## Prerequisites
- Python 3.13
- Poetry
- Docker
- Minikube (for Kubernetes)
- Dapr CLI

## Setup
1. Install dependencies: `make install`
2. Run locally: `make run-local`
3. Run with Docker Compose: `make run-docker`
4. Run on Kubernetes: `make run-k8s`

## Test
- Create an order: `curl -X POST http://localhost:8000/orders -d '{"order_id": "123"}'`
- Check logs for Pub/Sub and Workflow execution.
# FastAPI-Dapr POC
## Project Overview
This project is a Proof of Concept (POC) demonstrating the integration of FastAPI with Dapr for building microservices. It includes services such as `order-service`, `payment-service`, `workflow-service`, `subscriber-service`, and `delivery-service`, leveraging Dapr's Pub/Sub, State Management, and Workflow features for service communication and orchestration. The project supports both local development and Kubernetes deployment using k3d.

## Features
- **Microservices Architecture**: Multiple independent services built with FastAPI.
- **Dapr Integration**: Utilizes Dapr's Pub/Sub for messaging, State Management for persistence, and Workflow for orchestration.
- **Local Development**: Run services locally with Dapr CLI and Docker Compose.
- **Kubernetes Deployment**: Deploy to a k3d cluster with automated image builds and imports.
- **API Testing**: Supports testing via HTTP endpoints, with Swagger UI for API documentation.

## Project Structure
- `components/`: Dapr component YAML files (pubsub.yaml, statestore.yaml) for Pub/Sub and State Management.
- `k8s/`: Kubernetes deployment YAML files for services and resources.
- `apps/`: Source code for microservices (e.g., order_service, payment_service).
    - `main.py`: Entry point for each service.
- `Dockerfile`: Dockerfiles for building service images, with one in the root for `order-service` and others in `apps/<service>/`.
- `docker-compose.yml`: Configuration for local development with Docker Compose.
- `Makefile`: Automates build, deployment, and testing tasks.

## Prerequisites
To run this project, ensure the following tools are installed:
- Python >= 3.11
- Poetry for dependency management (`pip install poetry`)
- Dapr CLI for Dapr runtime
- Docker and Docker Compose
- k3d for lightweight Kubernetes deployment
- kubectl for Kubernetes management
- Helm for deploying Redis in k3d

## Installation
1. **Clone the Repository:**
    ```bash
    git clone https://github.com/ChenYuTingJerry/fastapi-dapr.git
    cd fastapi-dapr
    ```
2. **Install Python Dependencies:** Use Poetry to install dependencies:
    ```bash
    make install
    ```
3. Initialize Dapr: Set up the Dapr runtime, which automatically starts a Redis container:
    ```bash
    make init-dapr
    ```
   
## Running Locally
1. Start All Services: Launch services with Dapr sidecars using the configuration in `dapr.yaml`:
    ```bash
    make run-all
    ```
   Note: `dapr init` handles Redis setup, so no manual Redis container is needed.
2. Test the API: Run the test command to verify endpoints:
    ```bash
    make test
    ```
   
## Running on Kubernetes with k3d
1. **Deploy to k3d:** Deploy all components and services to a k3d cluster with a single command:
    ```bash
    make run-k3d
    ```
This command:
- Creates or starts a k3d cluster named `dapr-cluster` with `--port 8081:80@loadbalancer`, mapping LoadBalancer services' port 80 to `localhost:8081`.
- Installs Dapr on k3d.
- Deploys Redis via Helm.
- Applies Dapr components (`pubsub.yaml`, `statestore.yaml`) with k3d-specific Redis configuration.
- Builds Docker images using `docker-compose build` and imports them to k3d with `k3d image import`.
- Deploys services from `k8s/` to the cluster.
6. **Test the API:** Run tests on the k3d cluster:
    ```bash
    make test-k3d
    ```
## Troubleshooting
- **ErrImageNeverPull**: Ensure images are imported into k3d:
    ```bash
    k3d image import fastapi-dapr/order-service:latest -c dapr-cluster
    ```
  Verify images in k3d node:
    ```bash
    docker exec k3d-dapr-cluster-server-0 docker images | grep fastapi-dapr
    ```

## Contact
- For questions or support, create a GitHub issue or contact the maintainer at nmjk2000@gmail.com.


## Acknowledgments
- FastAPI for the web framework.
- Dapr for microservices runtime.
- k3d for lightweight Kubernetes.
- Poetry for dependency management.
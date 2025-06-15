# Variables
K3D_CLUSTER_NAME ?= dapr-cluster
IMAGE_PREFIX ?= fastapi-dapr

# Install dependencies
install:
	poetry install

# Run local services with Dapr
run-delivery:
	dapr run --app-id delivery-service --app-port 8004 --dapr-http-port 3504 \
	--resources-path ./components -- \
	poetry run gunicorn apps.delivery_service.app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8004 --log-level info

run-workflow:
	dapr run --app-id workflow-service --app-port 8006 --dapr-http-port 3506 \
	--resources-path ./components -- \
	poetry run gunicorn apps.workflow_service.app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8006 --log-level info

run-order:
	dapr run --app-id order-service --app-port 8001 --dapr-http-port 3501 \
	--resources-path ../../ -- \
	gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8001 --log-level info

run-payment:
	dapr run --app-id payment-service --app-port 8002 --dapr-http-port 3502 \
	--resources-path ./components -- \
	gunicorn apps.payment_service.app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8002 --log-level info

run-subscriber:
	dapr run --app-id subscriber-service --app-port 8003 --dapr-http-port 3503 \
	--resources-path ./components -- \
	poetry run gunicorn apps.subscriber_service.app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8003 --log-level info

# Initialize Dapr locally
init-dapr:
	dapr uninstall --all
	dapr init

# Run all services locally
run-all: init-dapr
	export REDIS_HOST=localhost:6379
	export REDIS_PASSWORD=""
	dapr run -f dapr.yaml

# Test local order creation
test:
	http POST http://0.0.0.0:8001/create

stop:
	dapr stop -f dapr.yaml
	dapr uninstall --all

# Ensure k3d cluster exists (create if not, start if stopped)
ensure-k3d-cluster:
	@if ! k3d cluster list | grep -q $(K3D_CLUSTER_NAME); then \
		k3d cluster create $(K3D_CLUSTER_NAME) --port 8081:80@loadbalancer; \
	else \
		k3d cluster start $(K3D_CLUSTER_NAME); \
	fi

# Install Dapr on k3d
install-dapr:
	dapr uninstall -k --all
	dapr init -k

# Deploy Dapr components
deploy-components:
	sed 's/value: "localhost:6379"/value: "redis-master.default.svc.cluster.local:6379"/' components/pubsub.yaml > components/pubsub-k8s.yaml
	sed 's/value: "localhost:6379"/value: "redis-master.default.svc.cluster.local:6379"/' components/statestore.yaml > components/statestore-k8s.yaml
	kubectl apply -f components/pubsub-k8s.yaml
	kubectl apply -f components/statestore-k8s.yaml

build-images:
	docker compose build
	for service in order-service payment-service subscriber-service workflow-service; do \
		k3d image import fastapi-dapr/$$service:latest -c $(K3D_CLUSTER_NAME); \
	done

# Deploy applications to k3d
deploy-applications:
	kubectl apply -f k8s/

deploy-redis:
	helm repo add bitnami https://charts.bitnami.com/bitnami
	helm repo update
	helm install redis bitnami/redis --namespace default --set master.persistence.enabled=false

# Run all steps for k3d deployment
run-k3d: ensure-k3d-cluster install-dapr deploy-redis deploy-components build-images deploy-applications

# Test k3d order creation
test-k3d:
	http POST http://localhost:8081/create

# Clean up k3d cluster
k3d-delete-cluster:
	helm delete redis
	k3d cluster delete $(K3D_CLUSTER_NAME)

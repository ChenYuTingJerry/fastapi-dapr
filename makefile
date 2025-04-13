install:
	poetry install

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

run-redis:
	docker-compose up -d redis

init-dapr:
	dapr uninstall --all
	dapr init

run-all:
	dapr run -f .

# 測試 create 訂單並觸發付款流程
test:
	http POST http://localhost:8001/create
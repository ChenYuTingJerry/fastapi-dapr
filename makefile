install:
	poetry install

run-order:
	dapr run --app-id order-service --app-port 8001 --dapr-http-port 3501 \
	--resources-path ./components -- \
	gunicorn apps.order_service.app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8001

run-payment:
	dapr run --app-id payment-service --app-port 8002 --dapr-http-port 3502 \
	--resources-path ./components -- \
	gunicorn apps.payment_service.app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8002

run-redis:
	docker-compose up -d redis

init-dapr:
	dapr uninstall --all
	dapr init

run-all:
	make -j2 run-payment run-order

# 測試 create 訂單並觸發付款流程
test:
	http POST http://localhost:8001/create
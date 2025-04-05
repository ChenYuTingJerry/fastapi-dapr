#!/bin/bash

# 使用 poetry run 以確保使用虛擬環境中的 Python 套件
export DAPR_HTTP_PORT=3500
export DAPR_GRPC_PORT=50001

# 啟動 Redis（如果沒使用 docker-compose）
docker run -d -p 6379:6379 --name redis-local redis

# 啟動 order_service (FastAPI)
poetry run dapr run --app-id order --app-port 8001 \
  --components-path ./dapr/components \
  -- uvicorn apps.order_service.main:app --host 0.0.0.0 --port 8001 &

# 啟動 payment_service (gRPC)
poetry run dapr run --app-id payment --app-port 50052 --app-protocol grpc \
  --components-path ./dapr/components \
  -- python apps/payment_service/main.py &

# 啟動 workflow_service
poetry run dapr run --app-id workflow \
  --components-path ./dapr/components \
  -- python apps/workflow_service/main.py &

wait

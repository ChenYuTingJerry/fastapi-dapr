APP_NAME=fastapi-in-ddd
TAG=latest
PORT=8000

dapr-run:
	dapr run --app-port 8000 --app-id hello-app --app-protocol http --dapr-http-port 3501 -- python main.py
	#gunicorn "main:app" -w 2 -k uvicorn.workers.UvicornWorker -b "0.0.0.0:8000"

local-run:
	docker run --rm -p $(PORT):$(PORT) -it $(APP_NAME):$(TAG)

build:
	DOCKER_BUILDKIT=1 docker build . -t $(APP_NAME):$(TAG)

k8s-deploy:
	skaffold dev -p python-app

k8s-undeploy:
	skaffold delete -p python-app

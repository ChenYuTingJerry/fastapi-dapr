APP_NAME=fastapi-in-ddd
TAG=latest
PORT=8000

local-run:
	gunicorn "main:app" -w 2 -k uvicorn.workers.UvicornWorker -b "0.0.0.0:8000"

run: build
	docker run --rm -p $(PORT):$(PORT) -it $(APP_NAME):$(TAG)

build:
	DOCKER_BUILDKIT=1 docker build . -t $(APP_NAME)
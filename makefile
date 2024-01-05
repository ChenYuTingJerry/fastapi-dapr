APP_NAME=fastapi-in-ddd
TAG=latest

local-run:
	gunicorn "main:app" -w 2 -k uvicorn.workers.UvicornWorker -b "0.0.0.0:5000"

run: build
	docker run --rm -p 8000:8000 -it $(APP_NAME):$(TAG)

build:
	DOCKER_BUILDKIT=1 docker build . -t $(APP_NAME)
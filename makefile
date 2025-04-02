.PHONY: run-local build-proto run-compose run-k8s

run-local:
	poetry install
	bash scripts/run_local.sh

build-proto:
	bash proto/build.sh

run-compose:
	docker-compose up --build

run-k8s:
	kubectl apply -f deployments/k8s/
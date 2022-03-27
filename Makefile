.ONESHELL:

build-backend-local-image:
	docker buildx bake -f docker-bake.hcl lorita-bot-backend-image-local

build-backend-release-image:
	DOCKER_CLI_EXPERIMENTAL=enabled docker buildx bake -f docker-bake.hcl lorita-bot-backend-release --push

build-run-backend-compose:
	COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose -f docker-compose.build.yml --env-file backend/.env up --build


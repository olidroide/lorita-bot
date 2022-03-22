.ONESHELL:

create-local-image:
	docker buildx create --name lorita-bot --driver docker-container --use
	docker buildx build --load -t lorita-bot .

create-and-push-image:
	docker buildx create --name lorita-bot --driver docker-container --use
	docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t lorita-bot:latest --no-cache --pull . --push

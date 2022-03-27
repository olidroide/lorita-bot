variable "TAG" {
    default = "latest"
}

group "default" {
    targets = ["lorita-bot-backend-dev"]
}

target "lorita-bot-backend-dev" {
    context = "."
    dockerfile = "backend/Dockerfile"
    tags = ["lorita-bot-backend:${TAG}"]
}

target "lorita-bot-backend-image-local" {
  inherits = ["lorita-bot-backend-dev"]
  output = ["type=docker"]
}

target "lorita-bot-backend-release" {
    inherits = ["lorita-bot-backend-dev"]
    platforms = [
    "linux/amd64",
    "linux/arm64",
    "linux/arm/v6",
    "linux/arm/v7",
    ]
}
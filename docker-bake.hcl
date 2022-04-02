variable "TAG" {
    default = "latest"
}

group "default" {
    targets = ["lorita-bot-backend-dev","lorita-bot-frontend-dev"]
}

target "lorita-bot-backend-dev" {
    context = "."
    dockerfile = "backend/Dockerfile"
    tags = ["lorita-bot-backend:${TAG}"]
}

target "lorita-bot-frontend-dev" {
    context = "."
    dockerfile = "frontend/Dockerfile"
    tags = ["lorita-bot-frontend:${TAG}"]
}

target "lorita-bot-backend-image-local" {
  inherits = ["lorita-bot-backend-dev"]
  output = ["type=docker"]
}

target "lorita-bot-frontend-image-local" {
  inherits = ["lorita-bot-frontend-dev"]
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

target "lorita-bot-frontend-release" {
    inherits = ["lorita-bot-backend-dev"]
    platforms = [
    "linux/amd64",
    "linux/arm64",
    "linux/arm/v6",
    "linux/arm/v7",
    ]
}
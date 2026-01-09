terraform {
  required_providers {
    docker = {
      source = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
    kubernetes = {
      source = "hashicorp/kubernetes"
      version = "~> 2.23.0"
    }
  }
}


resource "docker_image" "dataread" {
  name = "dataread"
  build {
    context = "${path.module}/.."
    dockerfile = "Dockerfile"
  }
}
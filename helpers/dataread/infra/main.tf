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
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.11.0"
    }
  }
}

provider "helm" {
  kubernetes {
    config_path = "~/.kube/config" # Adjust if needed
  }
}

# 1. Build the local image
resource "docker_image" "dataread" {
  name = "dataread:latest"
  build {
    context    = "${path.module}/../helpers/dataread"
    dockerfile = "Dockerfile"
  }
}

# 2. Deploy Postgres using Helm
resource "helm_release" "postgres" {
  name       = "postgres"
  repository = "https://charts.bitnami.com/bitnami"
  chart      = "postgresql"

  set {
    name  = "auth.postgresPassword"
    value = "password123"
  }
  set {
    name  = "auth.database"
    value = "ckad"
  }
}

# 3. Deploy your dataread Helper using Helm
resource "helm_release" "dataread" {
  name       = "dataread-app"
  chart      = "${path.module}/../helpers/dataread/charts/dataread"
  depends_on = [helm_release.postgres, docker_image.dataread]

  set {
    name  = "image.tag"
    value = "latest"
  }
  
  # Match the password set in the postgres release
  set {
    name  = "postgres.password"
    value = "password123"
  }
}
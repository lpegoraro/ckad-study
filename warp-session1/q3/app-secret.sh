kubectl create secret generic app-secret --from-literal=DB_USER="$(echo admin | base64)" --from-literal=DB_PASSWORD="$(echo super-secret-123 | base64)"

#!/bin/bash
set -e

echo "Stopping and removing containers, volumes, and networks..."

docker compose down -v || true

# Попробуем снова удалить сеть, если осталась
NETWORK_NAME="deploy_app-network"
if docker network inspect "$NETWORK_NAME" >/dev/null 2>&1; then
    echo "Trying to forcibly disconnect and remove lingering network: $NETWORK_NAME"
    for container in $(docker network inspect "$NETWORK_NAME" -f '{{range .Containers}}{{.Name}} {{end}}'); do
        echo "Disconnecting container $container from network..."
        docker network disconnect -f "$NETWORK_NAME" "$container" || true
    done
    docker network rm "$NETWORK_NAME" || true
fi

echo "Cleanup finished."

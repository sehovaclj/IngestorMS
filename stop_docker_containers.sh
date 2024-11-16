#!/bin/bash

# Constants
CONTAINER_NAME_PREFIX="ingestor_ms_simulation_container_"

# Function to print messages with UTC timestamp
log() {
    echo "$(date -u +'%Y-%m-%d %H:%M:%S.%3N') $1"
}

# Stop all containers matching the prefix
log "Stopping containers with prefix '${CONTAINER_NAME_PREFIX}'..."
for container in $(sudo docker ps -q --filter "name=${CONTAINER_NAME_PREFIX}"); do
    if ! sudo docker stop "$container" ; then
        log "Failed to stop container $container. Exiting..."
        exit 1
    fi
    log "Container $container stopped successfully."
done

log "All matching containers stopped successfully."
exit 0

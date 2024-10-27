# Variables
COMPOSE_FILE = docker-compose.yml

# Start the services with Docker Compose
up:
	docker compose -f $(COMPOSE_FILE) up -d

# Stop the services
down:
	docker compose -f $(COMPOSE_FILE) down

# Restart the services
restart: down up

# View logs from the services
logs:
	docker compose -f $(COMPOSE_FILE) logs -f

# Execute a shell in the IPFS container
shell-ipfs:
	docker exec -it ipfs_node sh

# Execute a shell in the IPFS Cluster container
shell-cluster:
	docker exec -it ipfs_cluster sh

# Get IPFS Node ID (required for setting CLUSTER_PEER)
node-id:
	docker exec ipfs_node ipfs id

# Remove all Docker images and volumes
clean:
	docker compose -f $(COMPOSE_FILE) down --volumes --remove-orphans

.PHONY: up down restart logs shell-ipfs shell-cluster node-id clean
# Variables
COMPOSE_FILE = docker-compose.yml

# Start the services with Docker Compose
up:
	python3 utils/generate_docker_compose.py
	docker compose -f $(COMPOSE_FILE) up -d
.PHONY: up

# Stop the services
down:
	docker compose -f $(COMPOSE_FILE) down
.PHONY: down

# Restart the services
restart: down up
.PHONY: restart

# View logs from the services
logs:
	docker compose -f $(COMPOSE_FILE) logs -f
.PHONY: logs

# Execute a shell in the IPFS container
shell-ipfs:
	docker exec -it ipfs_node sh
.PHONY: shell-ipfs

# Execute a shell in the IPFS Cluster container
shell-cluster:
	docker exec -it ipfs_cluster sh
.PHONY: shell-cluster

# Get IPFS Node ID
node-id:
	docker exec ipfs_node ipfs id
.PHONY: node-id

# Get IPFS Cluster ID
cluster-id:
	docker exec ipfs_cluster ipfs-cluster-ctl id
.PHONY: cluster-id

# Remove all Docker images and volumes
clean:
	docker compose -f $(COMPOSE_FILE) down --volumes --remove-orphans
.PHONY: clean
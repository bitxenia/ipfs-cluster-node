import json

with open("config.json") as config_file:
    config = json.load(config_file)

# Generate the docker compose with the given configuration
docker_compose_content = f"""services:

  ipfs_node:
    container_name: ipfs_node
    image: ipfs/kubo:release
    ports:
      - "4001:4001" # ipfs swarm
      - "5001:5001" # ipfs api
      - "8080:8080" # ipfs gateway
    volumes:
      - ./data/ipfs_data:/data/ipfs

  ipfs_cluster:
    container_name: ipfs_cluster
    image: ipfs/ipfs-cluster:latest
    depends_on:
      - ipfs_node
    environment:
      CLUSTER_PEERNAME: ipfs_cluster
      CLUSTER_SECRET: "{config['CLUSTER_SECRET']}"
      CLUSTER_IPFSHTTP_NODEMULTIADDRESS: /dns4/ipfs_node/tcp/5001
      CLUSTER_CRDT_TRUSTEDPEERS: '*' # Trust all peers in Cluster
      CLUSTER_RESTAPI_HTTPLISTENMULTIADDRESS: /ip4/0.0.0.0/tcp/9094 # expose API
      CLUSTER_MONITORPINGINTERVAL: 2s # Speed up peer discovery
    ports:
      - "9094:9094" # http api
      - "9095:9095" # proxy api
      - "9096:9096" # cluster swarm, other peers connect via this port
    volumes:
      - ./data/ipfs_cluster_data:/data/ipfs-cluster
    command: ["daemon", "--bootstrap", {', '.join(f'"{addr}"' for addr in config['PEERSTORE'])}]

volumes:
  ipfs_data:
  ipfs_cluster_data:
"""

with open("docker-compose.yml", "w") as compose_file:
    compose_file.write(docker_compose_content)

# Read the configuration from the .env file
config = {}
with open(".env", "r") as env_file:
    for line in env_file:
        key_and_value = line.strip().split("=")
        key = key_and_value[0]
        value = key_and_value[1] if len(key_and_value) > 1 else ""
        config[key] = value

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
      - ./{config['PUBLISH_DIRECTORY_NAME']}:/{config['PUBLISH_DIRECTORY_NAME']}
    command: ['daemon', '--init'{", '--enable-namesys-pubsub'" if config['ENABLE_IPNS_PUBSUB'] == 'true' else ""}]

  ipfs_cluster:
    container_name: ipfs_cluster
    image: ipfs/ipfs-cluster:latest
    depends_on:
      - ipfs_node
    environment:
      CLUSTER_PEERNAME: {config['CLUSTER_PEER_NAME']}
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
    {"command: ['daemon', '--bootstrap', " +  "'" + config["TRUSTED_PEERS"] + "'" + "]" if config['TRUSTED_PEERS'] else ""}

volumes:
  ipfs_data:
  {config['PUBLISH_DIRECTORY_NAME']}:
  ipfs_cluster_data:
"""

with open("docker-compose.yml", "w") as compose_file:
    compose_file.write(docker_compose_content)

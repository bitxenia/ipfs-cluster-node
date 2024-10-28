# ipfs-cluster-node

This repository provides a way to run an IPFS cluster node using Docker.

## Prerequisites

- [Docker](https://www.docker.com/) must be installed on your system.
- [Docker Compose](https://docs.docker.com/compose/) must also be installed.

## Setup

First copy the `.env.example` file to `.env` and set the environment variables as needed.

- `CLUSTER_SECRET` is the secret key used to authenticate the cluster nodes.
- `TRUSTED_PEERS` are the addresses of the all known trusted peers in the cluster.

```bash
cp .env.example .env
```

## Usage

A `Makefile` is provided to simplify the process of building and running the IPFS cluster node.

- `make run`: Start the IPFS cluster node.
- `make stop`: Stop the IPFS cluster node.
- `make restart`: Restart the IPFS cluster node.
- `make logs`: Show the logs of the IPFS cluster node.
- `make shell-ipfs`: Open a shell in the IPFS container.
- `make shell-cluster`: Open a shell in the IPFS cluster container.
- `make node-id`: Get the ID of the IPFS cluster node.
- `make cluster-id`: Get the ID of the IPFS cluster.
- `make clean`: Remove the IPFS cluster node.
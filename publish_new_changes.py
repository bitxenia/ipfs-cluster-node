import requests
import sys
import subprocess
import os

# Read the configuration from the .env file
config = {}
with open(".env", "r") as env_file:
    for line in env_file:
        key_and_value = line.strip().split("=")
        key = key_and_value[0]
        value = key_and_value[1] if len(key_and_value) > 1 else ""
        config[key] = value

# Configuration
CLUSTER_API = "http://localhost:9094"
IPFS_API = "http://localhost:5001"
IPNS_KEY_NAME = config["IPNS_KEY_NAME"]

container_name = "ipfs_node"  # Name of your Docker container running IPFS
cluster_container_name = (
    "ipfs_cluster"  # Name of your Docker container running IPFS Cluster
)


def add_to_ipfs(directory_path):
    # Command to add the directory to IPFS using docker exec
    command = [
        "docker",
        "exec",
        container_name,
        "ipfs",
        "add",
        "--quieter",
        "-r",
        directory_path,
    ]

    # Execute the command and capture the output
    try:
        cid = (
            subprocess.check_output(command, stderr=subprocess.STDOUT)
            .decode("utf-8")
            .rstrip()
        )
        print(f"Successfully added directory to IPFS: {cid}")
        return cid
    except subprocess.CalledProcessError as e:
        print("Error adding directory to IPFS:", e.output.decode("utf-8"))
        return None


def pin_to_cluster(cid):
    # Pin CID to IPFS Cluster using docker exec
    command = [
        "docker",
        "exec",
        cluster_container_name,
        "ipfs-cluster-ctl",
        "pin",
        "add",
        cid,
    ]

    try:
        subprocess.check_output(command, stderr=subprocess.STDOUT)
        print(f"Successfully pinned CID {cid} to the IPFS cluster.")
    except subprocess.CalledProcessError as e:
        print("Error pinning to cluster:", e.output.decode("utf-8"))


def update_ipns(cid):
    # Command to add the directory to IPFS using docker exec
    command = [
        "docker",
        "exec",
        container_name,
        "ipfs",
        "name",
        "publish",
        "--ttl=1m",
        f"/ipfs/{cid}",
    ]

    # Execute the command and capture the output
    try:
        response = subprocess.check_output(command, stderr=subprocess.STDOUT).decode(
            "utf-8"
        )
        print("Successfully updated IPNS:")
        print(response)
    except subprocess.CalledProcessError as e:
        print("Error updating IPNS:", e.output.decode("utf-8"))


def main():
    if len(sys.argv) < 2:
        print("Usage: python publish_new_changes.py <directory>")
        sys.exit(1)

    directory_path = sys.argv[1]

    # Step 1: Add the directory to IPFS
    cid = add_to_ipfs(directory_path)
    if cid:
        # Step 2: Pin the CID to the IPFS Cluster
        pin_to_cluster(cid)

        # Step 3: Update the IPNS record with the new CID
        update_ipns(cid)


if __name__ == "__main__":
    main()

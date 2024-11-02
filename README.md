# ipfs-cluster-node

Este repositorio proporciona una forma de rápida de ejecutar un nodo _trusted_ de un Cluster IPFS utilizando Docker. Como también una automatización para la publicación de un directorio al cluster y la actualización de un registro IPNS.

## Preequisitos

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Setup

Lo primero que hay que hacer es copiar el archivo `.env.example` a `.env` y configurar las variables de entorno según sea necesario.

Las configuraciones se dividen en dos grupos:

### Configuraciones de IPFS Cluster

- `CLUSTER_PEER_NAME` 
    - Es el nombre del nodo. Se utiliza para identificar el nodo en el cluster.
- `CLUSTER_SECRET`
    - Es la clave usada para autenticar y asegurar la comunicación entre los nodos del cluster. Se comparte entre todos los nodos del cluster.
    - Si se deja en blanco, se generará una clave aleatoria al iniciar el cluster por primera vez. Se puede obtener la clave en el `service.json` dentro de la data del cluster.
- `TRUSTED_PEERS`
    - Son las direcciones de los nodos _trusted_ en el cluster. Un nodo _trusted_ es un nodo que tiene permiso para realizar cambios al _pinset_ del cluster.
    - Las direcciones de los nodos _trusted_ deben estar separadas por comas.
    - Ejemplo: `<peer0_addr>,<peer1_addr>,...,<peerN_addr>`
    - Para obtener la dirección de un nodo, se puede ejecutar el comando `make cluster-id` en el nodo deseado y copiar la dirección del nodo que tenga formato `/ip4/<PublicIP>/tcp/9096/p2p/<PeerID>`. La IP pública se puede obtener con el comando `curl ifconfig.me`.

### Configuraciones de IPNS

- `ENABLE_IPNS_PUBSUB`
    - Habilita la publicación de registros IPNS utilizando el protocolo PubSub.
    - Por defecto, el valor es `true`.

- `IPNS_KEY_NAME`
    - Es el nombre de la clave utilizada para firmar los registros IPNS.
    - Si se deja en blanco, se generará una clave al iniciar el cluster por primera vez.

- `PUBLISH_DIRECTORY_NAME`
    - Es el nombre del directorio que se generará para poder publicar archivos al cluster.
    - Por defecto, el valor es `publish`.

## Uso

Un `Makefile` es proporcionado para simplificar el proceso de construcción y ejecución del nodo del cluster IPFS.

- `make run`: Inicia el nodo del cluster IPFS.
- `make stop`: Detiene el nodo del cluster IPFS.
- `make logs`: Muestra los logs del nodo del cluster IPFS.
- `make shell-ipfs`: Abre una terminal en el contenedor del nodo IPFS.
- `make shell-cluster`: Abre una terminal en el contenedor del cluster IPFS.
- `make node-id`: Obtiene el ID del nodo del cluster IPFS.
- `make cluster-id`: Obtiene el ID del cluster IPFS.

### Publicar un directorio al cluster y actualizar un registro IPNS

Para publicar un directorio al cluster y actualizar un registro IPNS, se puede utilizar el script `publish_new_changes.py`.

Primero es necesario copiar el directorio que se desea publicar al directorio `publish` dentro del directorio raíz del proyecto.

```bash
cp -r <directory> publish/
```

Luego, se debe ejecutar el script `publish_new_changes.py` con el nombre del directorio que se desea publicar.

```bash
python3 publish_new_changes.py <directory>
```
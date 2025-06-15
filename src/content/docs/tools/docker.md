---
title: Docker
description: Docker.
---

## Installation
```bash
# Update packages
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install -y docker.io docker-compose
# Verify installation
docker --version
docker-compose --version

# Enable & Start Docker
sudo systemctl enable docker
sudo systemctl start docker

# Add user to Docker group (avoid sudo for Docker)
sudo usermod -aG docker $USER
newgrp docker  # Apply changes without logout
```

## Images
```bash

# Build a Docker image with the given path of Dockerfile (if not named 'Dockerfile' in current dir) and the current directory as the build context
docker build -f <dockerfile_path> -t <image_name> .

# Print all the dangling images (untagged)
docker images -f dangling=true -q

# Remove all dangling images (images with no tags/names)
# List all images (-a), pipe to grep to find ones with "none",
# awk prints the 3rd column ($3) which is the image ID,
# pipe IDs to xargs docker rmi to remove those images
docker images -a | grep none | awk '{ print $3; }' | xargs docker rmi

# Alternative command to remove dangling images
# -f "dangling=true" filters for untagged images, -q returns just the IDs
docker rmi $(docker images -f "dangling=true" -q)

# Remove all Docker images forcefully (-f)
# $(docker images -aq) gets all image IDs (-a for all images, -q for quiet mode/IDs only)
docker rmi -f $(docker images -aq)

# Saves a Docker image to a file
docker save -o <file-name>.tar <image-name>:<image-tag>

# Load an image from a tar archive
docker load -i <file-name>.tar
```

## Containers
```bash
# Create and run a container from an image, with a custom name, publish a container’s port(s) to the host, mount volumes and automatic cleanup after exit
docker run --name <container_name> -p <host_port>:<container_port> -v <host_dir>:<container_dir> --rm <image_name>

docker run  <image_name>

# Open a shell inside a running container
docker exec -it <container_name> sh
docker exec -it <container_name> /bin/bash
# To exit
exit

# Execute a command in a running container
docker exec <command>
# e.g.
docker exec frontend npm install <package_name>

# Fetch and follow the logs of a container
docker logs -f <container_name>

# Stop and remove a container
docker container stop <container-name-or-id> | xargs docker rm

# To list currently running containers
docker ps

# List all docker containers (running and stopped)
docker ps --all

# Stop all running containers
# $(docker ps -aq) gets all container IDs
docker stop $(docker ps -aq)

# Stop and remove all the containers
docker stop $(docker ps -aq) | xargs docker rm

# Remove all stopped containers
docker container prune

# Remove all the volumes
docker volume rm $(docker volume ls -q)
```

## Docker-compose
```bash
# Start containers in detached mode (-d runs them in background)
docker compose up -d

# Build, (re)create, and start containers in detached mode (-d)
# --build: Force build images before starting containers
# --watch: Watch for file changes and update containers automatically
docker compose up --build --watch

# Open a shell inside a running container using docker-compose
docker compose exec <container_name> sh

# Execute psql command inside a running postgres container to list tables and their access privileges (\z shows table access privileges). The psql commands could be updated based on needs
docker exec -it $(docker-compose ps -q <container_name> ) psql -U <postgres_user_name> -c '\z'

# Fetch and follow the logs of all containers in docker-compose
docker compose logs -f

# Stop containers and remove volumes and images
docker compose down --volumes --rmi all  # Removes all images
docker compose down --volumes --rmi local # Removes only images that don't have a custom tag
```

## Miscellaneous

### Understanding Docker Port Mappings

When you see `0.0.0.0:4200->4200/tcp`, it means:
- The host machine is listening on port 4200 (left side)
- Traffic is being forwarded to port 4200 in the container (right side)
- The connection is successful and ports are properly mapped

If you only see `4200/tcp` without the arrow (`->`), it indicates:
- The container has exposed port 4200
- But no port mapping/publishing has been configured
- The port is not accessible from the host machine


### Angular: Monitor `src` Directory Changes

#### Options

1. Using inotify (for Windows hosts):
   - Edit `package.json` in the `"scripts"` section:
     ```json
     "scripts": {
       "start": "ng serve --host 0.0.0.0 --poll"
     }
     ```

2. Enable hot reload:
   - Add to Dockerfile:
     ```dockerfile
     EXPOSE 49153
     ```
   - Add to docker-compose.yml:
     ```yaml
     ports:
       - '49153:49153'
     ```

#### CMD arg in Dockerfile
The CMD instruction in a Dockerfile specifies the default command to run when starting a container. However:

- If you provide command arguments when running `docker run`, they will override the CMD instruction
- Example:
  ```dockerfile
  # Dockerfile
  CMD ["echo", "hello"]
  ```
  ```bash
  # Uses CMD instruction - prints "hello"
  docker run <image_name>

  # Overrides CMD - prints "world"
  docker run <image_name> echo world
  ```
- The ENTRYPOINT instruction can be used instead if you want a command that cannot be overridden

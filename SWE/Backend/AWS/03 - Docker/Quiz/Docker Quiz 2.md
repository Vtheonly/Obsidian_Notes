# Docker Quiz 2

This quiz covers lessons 3.1 through 8: Data Persistence/Volumes, Parent Images/Docker Hub, Layers/Image Efficiency, Dockerfile, .dockerignore, Container Management, docker exec, and Docker Compose.

## True/False

> [!question] Data inside a container's writable layer persists even after the container is deleted.
>> [!success]- Answer
>> False. The writable layer is destroyed when the container is removed. To persist data, you must use volumes or bind mounts.

> [!question] A named volume stores data on the host filesystem, managed by Docker.
>> [!success]- Answer
>> True. Named volumes are stored in Docker's managed area (e.g., `/var/lib/docker/volumes/`) and persist beyond the container lifecycle.

> [!question] A bind mount is the best choice for persisting database data in production.
>> [!success]- Answer
>> False. Named volumes are preferred for databases because they are managed by Docker and are more portable. Bind mounts are best suited for development where you need live code editing.

> [!question] The `latest` tag is the safest choice for production images because it always provides the most up-to-date software.
>> [!success]- Answer
>> False. The `latest` tag is unpredictable and can change without notice. Always pin a specific version tag (e.g., `node:17-alpine`) in production for consistency.

> [!question] Alpine-based images are always the best choice regardless of the application.
>> [!success]- Answer
>> False. Alpine uses `musl` instead of `glibc`, which can cause compatibility issues with some Python packages (e.g., NumPy, Pandas). Slim images may be a safer choice when Alpine compatibility is uncertain.

> [!question] When a layer in a Docker image changes, Docker must rebuild that layer and all layers below it.
>> [!success]- Answer
>> False. Docker rebuilds the changed layer and all layers **above** it (those that come after it in the Dockerfile). Layers below (before) the changed layer can be reused from cache.

> [!question] The `EXPOSE` instruction in a Dockerfile automatically publishes the port to the host machine.
>> [!success]- Answer
>> False. `EXPOSE` is documentation only. You must use the `-p` flag with `docker run` to actually publish the port.

> [!question] The `COPY . .` instruction in a Dockerfile will copy files listed in `.dockerignore` into the image.
>> [!success]- Answer
>> False. The `.dockerignore` file filters out matching files from the build context, so `COPY . .` will never see them.

> [!question] `docker start` creates a brand new container from an image.
>> [!success]- Answer
>> False. `docker start` wakes up an existing stopped container. `docker run` creates a new container.

> [!question] In Docker Compose, containers communicate with each other using IP addresses.
>> [!success]- Answer
>> False. Docker Compose provides automatic DNS resolution. Containers communicate using service names (e.g., `db`, `backend`) as hostnames.

## Multiple Choice

> [!question] Which volume type is best for live development where you edit code on your laptop and want changes reflected instantly in the container?
> a) Named volume
> b) Bind mount
> c) Anonymous volume
> d) tmpfs mount
>> [!success]- Answer
>> b) Bind mount. Bind mounts map a specific host directory into the container, so file changes on the host are immediately visible inside the container.

> [!question] What command lists all containers, including stopped ones?
> a) `docker ps`
> b) `docker ps -a`
> c) `docker list`
> d) `docker containers`
>> [!success]- Answer
>> b) `docker ps -a`. The `-a` flag shows all containers, not just running ones.

> [!question] What is the correct syntax for mapping host port 8080 to container port 80?
> a) `docker run -p 80:8080 image`
> b) `docker run -p 8080:80 image`
> c) `docker run --port 8080=80 image`
> d) `docker run -expose 8080:80 image`
>> [!success]- Answer
>> b) `docker run -p 8080:80 image`. The syntax is `-p HOST_PORT:CONTAINER_PORT`.

> [!question] Which Dockerfile instruction executes a command at build time to install dependencies?
> a) `CMD`
> b) `ENTRYPOINT`
> c) `RUN`
> d) `EXPOSE`
>> [!success]- Answer
>> c) `RUN`. The `RUN` instruction executes commands during the image build process, such as installing packages.

> [!question] Which Dockerfile instruction specifies the command to run when the container starts?
> a) `RUN`
> b) `CMD`
> c) `COPY`
> d) `WORKDIR`
>> [!success]- Answer
>> b) `CMD`. The `CMD` instruction defines the default command executed when a container is started from the image.

> [!question] Why should `node_modules` be listed in `.dockerignore`?
> a) To reduce the number of files Docker has to track
> b) Because packages compiled for macOS/Windows may not work inside a Linux container
> c) Because npm install is deprecated
> d) It should not be; node_modules must always be copied
>> [!success]- Answer
>> b) Because packages compiled for macOS/Windows may not work inside a Linux container. Dependencies should be installed fresh inside the image using `RUN npm install`.

> [!question] What does the `-it` flag do in `docker exec -it <container> /bin/bash`?
> a) Installs tools inside the container
> b) Keeps STDIN open and allocates a TTY for interactive terminal access
> c) Ignores terminal errors
> d) Increases the container's timeout
>> [!success]- Answer
>> b) Keeps STDIN open and allocates a TTY for interactive terminal access. `-i` keeps STDIN open; `-t` allocates a pseudo-terminal.

> [!question] What is the purpose of `depends_on` in a Docker Compose file?
> a) It installs dependencies inside the container
> b) It specifies the build order, ensuring a dependent service starts first
> c) It downloads required images from Docker Hub
> d) It creates a network bridge between services
>> [!success]- Answer
>> b) It specifies the build order, ensuring a dependent service starts first. For example, `depends_on: - db` ensures the database starts before the backend.

> [!question] Which command stops and removes all containers, networks, and images defined in a Docker Compose file?
> a) `docker-compose stop`
> b) `docker-compose down`
> c) `docker-compose rm`
> d) `docker-compose prune`
>> [!success]- Answer
>> b) `docker-compose down`. This stops and removes containers, networks, and optionally images and volumes defined in the Compose configuration.

> [!question] What is the first instruction in every Dockerfile?
> a) `RUN`
> b) `WORKDIR`
> c) `FROM`
> d) `COPY`
>> [!success]- Answer
>> c) `FROM`. Every Dockerfile must begin with a `FROM` instruction that specifies the parent (base) image.

> [!question] What does `WORKDIR /app` do in a Dockerfile?
> a) Creates a volume at /app
> b) Sets the working directory for all subsequent instructions inside the container image
> c) Exposes port /app
> d) Copies files from /app on the host
>> [!success]- Answer
>> b) Sets the working directory for all subsequent instructions inside the container image. It creates the directory if it does not exist and changes into it.

## Matching

> [!question] Match each Docker concept with its correct description.
>> [!example] Group A
>> a) Named Volume
>> b) Bind Mount
>> c) Layer Cache
>> d) `.dockerignore`
>> e) `docker exec`
>> f) `docker system prune`
>> g) `depends_on`
>> h) Service Name (Compose)
>> i) `alpine` tag
>> j) `RUN` vs `CMD`
>
>> [!example] Group B
>> n) Determines the order of service startup in Docker Compose
>> o) Reuses unchanged layers to speed up image rebuilds
>> p) Prevents unwanted files from entering the Docker build context
>> q) Docker-managed storage that persists data beyond the container lifecycle
>> r) Maps a specific host directory into the container for live development
>> s) Runs a new process inside an already running container
>> t) Ultra-lightweight Linux distribution used as a base image variant
>> u) Build-time execution vs. runtime execution
>> v) Used as a hostname for inter-container communication in Compose
>> w) Cleans up all stopped containers, dangling images, and unused networks
>
>> [!success]- Answer
>> a) -> q)
>> b) -> r)
>> c) -> o)
>> d) -> p)
>> e) -> s)
>> f) -> w)
>> g) -> n)
>> h) -> v)
>> i) -> t)
>> j) -> u)

---

Related: [[3.1 Data Persistence (Volumes)]] | [[4. Parent Images and Docker Hub]] | [[5. The Dockerfile]] | [[8. Docker Compose]]

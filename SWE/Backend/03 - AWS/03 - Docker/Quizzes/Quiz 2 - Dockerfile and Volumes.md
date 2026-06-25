# Quiz 2 - Dockerfile and Volumes

> [!info] About This Quiz
> This quiz covers [[3. Images and Containers]], [[3.1 Image Layers and Storage Drivers]], [[3.2 Volumes and Bind Mounts]], [[4. The Dockerfile]], [[4.1 The .dockerignore File]], and [[4.2 Multi-Stage Builds]].

Related: [[3. Images and Containers]] | [[3.2 Volumes and Bind Mounts]] | [[4. The Dockerfile]] | [[Quiz 1 - Containers and Virtualization]]

---

## Section A — True or False

> [!question] 1. Data inside a container's writable layer persists even after the container is deleted.
>> [!success]- Answer
>> **False.**
>> The writable layer is destroyed when the container is removed (`docker rm`). To persist data across container deletions, you must use **volumes** (named volumes, bind mounts, or tmpfs). The writable layer is tied to the container's lifecycle — it exists only as long as the container exists.

> [!question] 2. A named volume stores data on the host filesystem, managed by Docker.
>> [!success]- Answer
>> **True.**
>> Named volumes live on the host (e.g., `/var/lib/docker/volumes/<name>/_data` on Linux) but are managed by Docker. You refer to them by name (e.g., `pgdata`), not by path. They persist beyond the container's lifecycle and are portable across hosts (you can back them up, restore them, and migrate them).

> [!question] 3. A bind mount is the best choice for persisting database data in production.
>> [!success]- Answer
>> **False.**
>> Named volumes are preferred for production databases because:
>> - They are managed by Docker (clean lifecycle, `docker volume` commands work).
>> - They are portable across hosts (no hardcoded path).
>> - They avoid permission issues (the container's UID is the only one that needs access).
>> - Bind mounts couple the container to a specific host path and can cause permission issues with host UIDs.

> [!question] 4. The `latest` tag is the safest choice for production images because it always provides the most up-to-date software.
>> [!success]- Answer
>> **False.**
>> The `latest` tag is unpredictable — it can change without notice when the image maintainer pushes a new version. This breaks reproducibility: today's `node:latest` is Node 22, tomorrow it might be Node 23 with breaking changes. Always pin to a specific version tag (e.g., `node:18.19-alpine3.19`) for production. For even stronger guarantees, pin by digest (`node@sha256:abc123...`).

> [!question] 5. Alpine-based images are always the best choice regardless of the application.
>> [!success]- Answer
>> **False.**
>> Alpine uses `musl` instead of `glibc`. Many Python packages with C extensions (NumPy, Pandas, lxml) and some Node packages with native bindings do not have prebuilt musl wheels and must be compiled from source — which requires installing `gcc`, `musl-dev`, etc., and takes much longer than on Debian-based images. In those cases, `python:3.12-slim` or `node:18-slim` (Debian-based) is a safer choice. Always test your app on Alpine before committing.

> [!question] 6. When a layer in a Docker image changes, Docker must rebuild that layer and all layers below it.
>> [!success]- Answer
>> **False.**
>> Docker rebuilds the changed layer and all layers **above** it (those that come after it in the Dockerfile). Layers below (before) the changed layer can be reused from cache. This is why you should put rarely-changing instructions (like dependency installs) early in the Dockerfile — they invalidate less when code changes.

> [!question] 7. The `EXPOSE` instruction in a Dockerfile automatically publishes the port to the host machine.
>> [!success]- Answer
>> **False.**
>> `EXPOSE` is **documentation only** — it tells Docker and orchestration systems which port the container intends to listen on, but it does not actually publish anything. You still need `-p host_port:container_port` on `docker run` (or the `ports:` section in Compose) to make the port reachable from the host.

> [!question] 8. The `COPY . .` instruction in a Dockerfile will copy files listed in `.dockerignore` into the image.
>> [!success]- Answer
>> **False.**
>> The `.dockerignore` file filters out matching files from the build context **before** `COPY` runs. So `COPY . .` will never see the ignored files. This is the entire point of `.dockerignore` — it prevents unwanted files (like `node_modules`, `.env`, `.git`) from entering the image.

> [!question] 9. `docker start` creates a brand new container from an image.
>> [!success]- Answer
>> **False.**
>> `docker start` wakes up an existing stopped container — it preserves the container's ID, logs, and writable layer. `docker run` is the command that creates a brand new container (it is equivalent to `docker create` + `docker start`).

> [!question] 10. In Docker Compose, containers communicate with each other using IP addresses.
>> [!success]- Answer
>> **False.**
>> Docker Compose creates a user-defined bridge network and provides automatic DNS resolution. Containers communicate using **service names** (e.g., `db`, `backend`) as hostnames. You write `host=db` in your database connection config, not `host=172.18.0.3`. This is one of Compose's most powerful features.

---

## Section B — Multiple Choice

> [!question] 11. Which volume type is best for live development where you edit code on your laptop and want changes reflected instantly in the container?
> a) Named volume
> b) Bind mount
> c) Anonymous volume
> d) tmpfs mount
>> [!success]- Answer
>> **b) Bind mount.**
>> Bind mounts map a specific host directory into the container. When you edit a file on the host, the change is immediately visible inside the container (because they are the same file). Named volumes are managed by Docker and not easily editable from the host. `tmpfs` is in-memory only.
>> Example: `docker run -v $(pwd)/src:/app/src node-app`

> [!question] 12. What command lists all containers, including stopped ones?
> a) `docker ps`
> b) `docker ps -a`
> c) `docker list`
> d) `docker containers`
>> [!success]- Answer
>> **b) `docker ps -a`.**
>> The `-a` (or `--all`) flag shows all containers, not just running ones. Without `-a`, `docker ps` shows only currently running containers.

> [!question] 13. What is the correct syntax for mapping host port 8080 to container port 80?
> a) `docker run -p 80:8080 image`
> b) `docker run -p 8080:80 image`
> c) `docker run --port 8080=80 image`
> d) `docker run -expose 8080:80 image`
>> [!success]- Answer
>> **b) `docker run -p 8080:80 image`.**
>> The syntax is `-p HOST_PORT:CONTAINER_PORT`. So `8080:80` maps host port 8080 to container port 80. You access the app at `localhost:8080`; Docker forwards the traffic to the container's port 80.

> [!question] 14. Which Dockerfile instruction executes a command at build time to install dependencies?
> a) `CMD`
> b) `ENTRYPOINT`
> c) `RUN`
> d) `EXPOSE`
>> [!success]- Answer
>> **c) `RUN`.**
>> `RUN` executes a command during the build process and the result (filesystem changes) becomes a new layer in the image. Use it for installing packages, compiling code, generating files, etc. `CMD` and `ENTRYPOINT` specify what to run when the container starts (not build time).

> [!question] 15. Which Dockerfile instruction specifies the command to run when the container starts?
> a) `RUN`
> b) `CMD`
> c) `COPY`
> d) `WORKDIR`
>> [!success]- Answer
>> **b) `CMD`.**
>> `CMD` defines the default command executed when a container is started from the image. It does not run during the build. Use exec form (`CMD ["node", "server.js"]`) for proper signal handling.

> [!question] 16. Why should `node_modules` be listed in `.dockerignore`?
> a) To reduce the number of files Docker has to track
> b) Because packages compiled for macOS/Windows may not work inside a Linux container
> c) Because npm install is deprecated
> d) It should not be; `node_modules` must always be copied
>> [!success]- Answer
>> **b) Because packages compiled for macOS/Windows may not work inside a Linux container.**
>> Some npm packages (e.g., `bcrypt`, `sharp`, `node-sass`) contain native binaries compiled for the OS where they were installed. If you `npm install` on macOS and then `COPY . .` to copy `node_modules` into a Linux container, those binaries will not run — they crash with "exec format error" or "wrong ELF class." The fix is to ignore `node_modules` and run `RUN npm install` inside the image, where dependencies are compiled for Linux.

> [!question] 17. What does the `-it` flag do in `docker exec -it <container> /bin/bash`?
> a) Installs tools inside the container
> b) Keeps STDIN open and allocates a TTY for interactive terminal access
> c) Ignores terminal errors
> d) Increases the container's timeout
>> [!success]- Answer
>> **b) Keeps STDIN open and allocates a TTY for interactive terminal access.**
>> - `-i` (interactive) keeps STDIN open so the container can receive your keyboard input.
>> - `-t` (tty) allocates a pseudo-terminal so the shell has proper formatting (colors, cursor, tab completion).
>> Without `-it`, you can run a single command but cannot have an interactive shell session.

> [!question] 18. What is the purpose of `depends_on` in a Docker Compose file?
> a) It installs dependencies inside the container
> b) It specifies the build order, ensuring a dependent service starts first
> c) It downloads required images from Docker Hub
> d) It creates a network bridge between services
>> [!success]- Answer
>> **b) It specifies the build order, ensuring a dependent service starts first.**
>> `depends_on: [db]` tells Compose to start the `db` service before this one. Note that `depends_on` only waits for the container to start — not for the service to be ready. Use the long form (`condition: service_healthy`) with a healthcheck to wait for actual readiness.

> [!question] 19. Which command stops and removes all containers, networks, and images defined in a Docker Compose file?
> a) `docker-compose stop`
> b) `docker-compose down`
> c) `docker-compose rm`
> d) `docker-compose prune`
>> [!success]- Answer
>> **b) `docker-compose down`.**
>> `down` stops and removes containers, networks, and (optionally) images and volumes. Add `-v` to also remove named volumes (destructive). Add `--rmi all` to also remove images.

> [!question] 20. What is the first instruction in every Dockerfile?
> a) `RUN`
> b) `WORKDIR`
> c) `FROM`
> d) `COPY`
>> [!success]- Answer
>> **c) `FROM`.**
>> Every Dockerfile must begin with `FROM`, which specifies the parent image to build on. The only exception is when you use ARG before FROM (for variable base image selection): `ARG VERSION=18` then `FROM node:${VERSION}`.

> [!question] 21. What does `WORKDIR /app` do in a Dockerfile?
> a) Creates a volume at /app
> b) Sets the working directory for all subsequent instructions inside the container image
> c) Exposes port /app
> d) Copies files from /app on the host
>> [!success]- Answer
>> **b) Sets the working directory for all subsequent instructions inside the container image.**
>> `WORKDIR /app` creates the directory if it does not exist, then changes into it. All subsequent `RUN`, `COPY`, `CMD`, etc. operate relative to `/app`. Without `WORKDIR`, you would need to use absolute paths everywhere or chain `cd` commands (which is fragile).

---

## Section C — Matching

> [!question] 22. Match each Docker concept with its correct description.
>
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
>>
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
>> a) Named Volume → **q)** Docker-managed storage that persists data beyond the container lifecycle.
>> b) Bind Mount → **r)** Maps a specific host directory into the container for live development.
>> c) Layer Cache → **o)** Reuses unchanged layers to speed up image rebuilds.
>> d) `.dockerignore` → **p)** Prevents unwanted files from entering the Docker build context.
>> e) `docker exec` → **s)** Runs a new process inside an already running container.
>> f) `docker system prune` → **w)** Cleans up all stopped containers, dangling images, and unused networks.
>> g) `depends_on` → **n)** Determines the order of service startup in Docker Compose.
>> h) Service Name (Compose) → **v)** Used as a hostname for inter-container communication in Compose.
>> i) `alpine` tag → **t)** Ultra-lightweight Linux distribution used as a base image variant.
>> j) `RUN` vs `CMD` → **u)** Build-time execution vs. runtime execution.

---

## Section D — Deep Conceptual Questions

> [!question] 23. Explain the difference between `COPY app.py /app` and `COPY app.py /app/`. What happens if `/app` does not exist?
>> [!success]- Answer
>> - **`COPY app.py /app`**: If `/app` does not exist, Docker creates a directory `/app` and copies `app.py` into it → `/app/app.py`. If `/app` already exists as a directory, `app.py` is copied into it → `/app/app.py`. If `/app` already exists as a file, Docker **overwrites** it with `app.py`.
>> - **`COPY app.py /app/`**: The trailing slash explicitly says "this is a directory." Docker creates `/app` as a directory (if it does not exist) and copies `app.py` into it → `/app/app.py`. If `/app` exists as a file, the build fails with an error.
>>
>> **Recommendation**: Always use the trailing slash when copying into a directory, to make your intent explicit and avoid accidentally overwriting a file.

> [!question] 24. Why is it important to copy `package.json` (or `requirements.txt`, `go.mod`, etc.) **before** copying the rest of the source code in a Dockerfile?
>> [!success]- Answer
>> This is the standard layer caching optimization.
>>
>> If you do `COPY . .` first, then `RUN npm install`:
>> - Any change to any source file invalidates the `COPY . .` layer.
>> - Which invalidates the `RUN npm install` layer.
>> - So every code change triggers a full `npm install` (which can take minutes).
>>
>> If you copy `package.json` first, then `npm install`, then `COPY . .`:
>> - Code changes only invalidate the `COPY . .` layer.
>> - The `npm install` layer is cached as long as `package.json` has not changed.
>> - Rebuilds take seconds instead of minutes.
>>
>> ```dockerfile
>> # GOOD order
>> COPY package*.json ./
>> RUN npm install
>> COPY . .
>> ```

> [!question] 25. A colleague runs `docker run -v pgdata:/var/lib/postgresql/data postgres` and is confused that the volume appears "hidden" on the host. Explain what a Docker volume actually is and where it lives.
>> [!success]- Answer
>> A Docker named volume is a directory on the host filesystem, but it is **managed by Docker** — Docker decides where it lives and you normally do not interact with the path directly.
>>
>> On Linux, named volumes live under `/var/lib/docker/volumes/<volume_name>/_data`. So the `pgdata` volume's actual path is `/var/lib/docker/volumes/pgdata/_data`.
>>
>> You can inspect it:
>> ```bash
>> docker volume inspect pgdata
>> # {
>> #   "CreatedAt": "...",
>> #   "Driver": "local",
>> #   "Labels": null,
>> #   "Mountpoint": "/var/lib/docker/volumes/pgdata/_data",
>> #   "Name": "pgdata",
>> #   "Options": null,
>> #   "Scope": "local"
>> # }
>> ```
>>
>> It is not encrypted, not magical — it is a normal directory. But Docker abstracts it so you treat it as a managed resource (`docker volume ls`, `docker volume rm`, etc.) rather than fiddling with the host path.
>>
>> Contrast with **bind mounts**, where you explicitly choose the host path. Bind mounts are visible and editable; named volumes are managed and abstracted.

> [!question] 26. Explain what `EXPOSE 3000` in a Dockerfile does and does not do, and how to actually make port 3000 reachable from the host.
>> [!success]- Answer
>> `EXPOSE 3000`:
>> - **Does**: Document that the container intends to listen on port 3000. This is metadata in the image; it shows up in `docker inspect` and is used by orchestration systems (e.g., `docker run -P` publishes all exposed ports to random host ports).
>> - **Does not**: Actually publish the port. The port is **not** reachable from the host just because of `EXPOSE`.
>>
>> To make port 3000 reachable from the host:
>> ```bash
>> docker run -p 3000:3000 myapp
>> # or, bind to localhost only:
>> docker run -p 127.0.0.1:3000:3000 myapp
>> ```
>>
>> Without `-p`, the container is reachable only from inside its Docker network, not from the host.

> [!question] 27. You see the following Dockerfile. Identify three problems and suggest fixes.
> ```dockerfile
> FROM node:latest
> COPY . .
> RUN npm install
> WORKDIR /app
> EXPOSE 3000
> CMD node server.js
> ```
>> [!success]- Answer
>> **Problem 1: `FROM node:latest`**
>> The `latest` tag is a moving target. Today's build might use Node 22, tomorrow Node 23. Pin to a specific version: `FROM node:18.19-alpine3.19`.
>>
>> **Problem 2: `COPY . .` before `RUN npm install` and `WORKDIR`**
>> - `COPY . .` is run before `WORKDIR /app`, so files are copied into `/` (the root of the image filesystem), not `/app`.
>> - `COPY . .` is run before `RUN npm install`, which means any code change invalidates the install cache (slow rebuilds).
>> - Without `.dockerignore`, `COPY . .` will also copy `node_modules` (potentially wrong-architecture binaries) and `.env` (secrets).
>>
>> **Fix**: Reorder and use `.dockerignore`:
>> ```dockerfile
>> FROM node:18.19-alpine3.19
>> WORKDIR /app
>> COPY package*.json ./
>> RUN npm install
>> COPY . .
>> EXPOSE 3000
>> CMD ["node", "server.js"]
>> ```
>>
>> **Problem 3: `CMD node server.js` (shell form)**
>> Shell form runs the command via `/bin/sh -c "node server.js"`, making `/bin/sh` PID 1 instead of `node`. This breaks signal handling — `docker stop` sends SIGTERM to `/bin/sh`, which does not forward it to `node`, so the container has to be SIGKILL'd after the 10-second timeout.
>>
>> **Fix**: Use exec form: `CMD ["node", "server.js"]`.
>>
>> **Bonus problems**:
>> - The container runs as root. Add a non-root user.
>> - No `HEALTHCHECK` defined.

> [!question] 28. Explain the difference between `RUN`, `CMD`, and `ENTRYPOINT`. When would you use each?
>> [!success]- Answer
>> - **`RUN`**: Executes a command at **build time**. The result is a new layer in the image. Use it to install packages, compile code, generate files. Example: `RUN apt-get install -y curl`.
>> - **`CMD`**: Specifies the default command to run when the container starts. Can be overridden by `docker run` arguments. Use it for the default startup command. Example: `CMD ["node", "server.js"]`.
>> - **`ENTRYPOINT`**: Specifies the executable that **always** runs when the container starts. `docker run` arguments are **appended** to it (not overridden). Use it when the container is a "wrapper" around a specific executable.
>>
>> Common patterns:
>> - Simple app: `CMD ["node", "server.js"]` (overridable).
>> - Tool wrapper: `ENTRYPOINT ["git"]` and `CMD ["--help"]`. Then `docker run git-image status` runs `git status`.
>> - Flexible app: `ENTRYPOINT ["node"]` and `CMD ["server.js"]`. Then `docker run myapp` runs `node server.js`, and `docker run myapp --inspect` runs `node --inspect` (overrides the CMD args).
>>
>> Always use exec form (JSON array syntax) for `CMD` and `ENTRYPOINT` to ensure proper signal handling.

---

## Section E — Scenario-Based

> [!question] 29. Your team has a Node.js app that runs fine in development but crashes in the Docker container with `Error: Cannot find module 'express'`. What are the most likely causes?
>> [!success]- Answer
>> **Cause 1: `node_modules` not installed in the image**
>> Your Dockerfile might be missing `RUN npm install`, or it might be installing to the wrong directory.
>>
>> **Cause 2: `COPY . .` copied host `node_modules` (wrong architecture)**
>> If your `.dockerignore` does not exclude `node_modules`, `COPY . .` will copy your macOS/Windows-installed `node_modules` into the Linux container. Some packages (like `express` itself, which is pure JS) work fine, but native modules do not. Even pure JS modules might have transitive native deps.
>>
>> **Cause 3: Working directory mismatch**
>> `WORKDIR /app` followed by `COPY . .` puts files in `/app`. But if your `package.json` is somewhere else (or your `node_modules` is installed in a different path), Node cannot find them.
>>
>> **Cause 4: `npm install --production` skipped devDependencies**
>> If `express` is in `devDependencies` (unusual, but possible) and you install with `--only=production`, it will not be installed.
>>
>> **Diagnosis**:
>> ```bash
>> docker exec -it <container> sh
>> $ ls /app/node_modules | grep express    # is express there?
>> $ cat /app/package.json | grep express   # is it in dependencies?
>> ```

> [!question] 30. A container keeps restarting every 30 seconds. The logs show a database connection error: "Could not connect to db:5432." Your Compose file has `depends_on: [db]`. What is wrong, and how do you fix it?
>> [!success]- Answer
>> **The problem**: `depends_on: [db]` only waits for the `db` container to **start** — not for PostgreSQL to actually be **ready to accept connections**. Postgres takes a few seconds to initialize (loading the data directory, opening WAL files, etc.). The backend starts before Postgres is ready, fails to connect, crashes, and Compose's default restart policy (or yours) restarts it.
>>
>> **The fix**: Use the long form of `depends_on` with `condition: service_healthy`, and add a `healthcheck` to the `db` service:
>>
>> ```yaml
>> services:
>>   db:
>>     image: postgres:15
>>     healthcheck:
>>       test: ["CMD-SHELL", "pg_isready -U postgres"]
>>       interval: 5s
>>       timeout: 3s
>>       retries: 10
>>       start_period: 10s
>>
>>   backend:
>>     build: ./backend
>>     depends_on:
>>       db:
>>         condition: service_healthy
>>     restart: on-failure
>> ```
>>
>> Now Compose will not start the backend until the `db` healthcheck passes (i.e., Postgres is actually ready). The `restart: on-failure` covers any race conditions during the brief window between "healthy" and "actually accepting connections."

---

Related: [[3. Images and Containers]] | [[3.2 Volumes and Bind Mounts]] | [[4. The Dockerfile]] | [[Quiz 3 - Networking and Compose]]

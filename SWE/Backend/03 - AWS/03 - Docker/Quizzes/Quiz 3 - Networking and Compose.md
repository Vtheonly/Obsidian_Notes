# Quiz 3 - Networking and Compose

> [!info] About This Quiz
> This quiz covers [[5. Container Lifecycle and Management]], [[6. Docker Networking]], [[6.1 Custom Networks and DNS]], [[7. Docker Compose]], and [[8. Docker Security]].

Related: [[5. Container Lifecycle and Management]] | [[6. Docker Networking]] | [[7. Docker Compose]] | [[8. Docker Security]] | [[Quiz 2 - Dockerfile and Volumes]]

---

## Section A — True or False

> [!question] 1. Containers on the default `bridge` network can resolve each other by container name.
>> [!success]- Answer
>> **False.**
>> The default `bridge` network does **not** support DNS-based name resolution. To resolve containers by name, you must create a user-defined bridge network with `docker network create` and attach containers to it.

> [!question] 2. The `-p 8080:80` flag maps the container's port 8080 to the host's port 80.
>> [!success]- Answer
>> **False.**
>> The format is `-p HOST_PORT:CONTAINER_PORT`. So `-p 8080:80` maps the host's port 8080 to the container's port 80. You access the app at `localhost:8080`; Docker forwards the traffic to the container's port 80.

> [!question] 3. Multiple containers can all listen on port 80 internally, as long as they are published to different host ports.
>> [!success]- Answer
>> **True.**
>> Each container has its own network namespace, so port 80 inside each is independent. You can run `docker run -p 8081:80 web1`, `docker run -p 8082:80 web2`, `docker run -p 8083:80 web3` — three containers, all listening on 80 internally, but published to different host ports.

> [!question] 4. `docker exec` creates a new container to run a command.
>> [!success]- Answer
>> **False.**
>> `docker exec` starts a new process **inside an already-running container**. It does not create a new container. To create a new container, use `docker run` (or `docker create` + `docker start`).

> [!question] 5. In Docker Compose, services can communicate with each other using `localhost`.
>> [!success]- Answer
>> **False.**
>> Each service runs in its own container with its own network namespace. `localhost` inside one container refers to **that container**, not the host and not other containers. Services must communicate using **service names** (e.g., `host=db`), which Docker's DNS server resolves.

> [!question] 6. The `host` network driver gives the container access to the host's network stack with no isolation.
>> [!success]- Answer
>> **True.**
>> With `--network host`, the container shares the host's network interfaces, routing table, and ports. There is no NAT, no port mapping needed, and no isolation. Useful for performance-critical apps on Linux, but breaks on macOS/Windows (because the "host" is actually a Linux VM, not your Mac/Windows machine).

> [!question] 7. `--privileged` is the recommended way to run containers that need elevated permissions.
>> [!success]- Answer
>> **False.**
>> `--privileged` is **never recommended**. It disables almost all of Docker's isolation: grants all capabilities, disables seccomp, gives access to all host devices. A privileged container can typically escape to the host in seconds. The recommended approach is to drop all capabilities and add back only what you need: `--cap-drop=ALL --cap-add=NET_BIND_SERVICE`.

> [!question] 8. Docker's embedded DNS server is at `127.0.0.11` inside containers on user-defined networks.
>> [!success]- Answer
>> **True.**
>> On user-defined bridge and overlay networks, Docker configures each container's `/etc/resolv.conf` to use `127.0.0.11` as the nameserver. This is Docker's embedded DNS server, which resolves container names, network aliases, and Compose service names.

> [!question] 9. `docker-compose down -v` removes named volumes defined in the Compose file.
>> [!success]- Answer
>> **True.**
>> The `-v` (or `--volumes`) flag tells Compose to also remove named volumes. This is **destructive** — it deletes your database data. Only use `-v` when you want a clean slate.

> [!question] 10. The `HEALTHCHECK` instruction in a Dockerfile is required for the container to start.
>> [!success]- Answer
>> **False.**
>> `HEALTHCHECK` is optional. The container starts fine without it. However, without a healthcheck, Docker (and orchestrators like ECS, Kubernetes) cannot tell when your application is hung (as opposed to crashed). Adding `HEALTHCHECK` is a best practice for production images.

---

## Section B — Multiple Choice

> [!question] 11. Which network driver provides DNS-based service discovery by container name?
> a) `host`
> b) `bridge` (default)
> c) User-defined `bridge`
> d) `none`
>> [!success]- Answer
>> **c) User-defined `bridge`.**
>> The default `bridge` does not support DNS. Only user-defined bridge networks (created with `docker network create`) provide the embedded DNS server at `127.0.0.11` that resolves container names.

> [!question] 12. What is the exit code that indicates a container was OOM-killed?
> a) 0
> b) 1
> c) 127
> d) 137
>> [!success]- Answer
>> **d) 137.**
>> 137 = 128 + 9, meaning the process was killed by signal 9 (SIGKILL). The most common cause is the kernel's OOM killer terminating the process because the container exceeded its memory limit. Confirm with `docker inspect <container> --format '{{.State.OOMKilled}}'`.

> [!question] 13. Which flag publishes all `EXPOSE`'d ports to random host ports?
> a) `-p`
> b) `-P` (capital)
> c) `--publish-all`
> d) Both b and c
>> [!success]- Answer
>> **d) Both b and c.**
>> `-P` is the short form; `--publish-all` is the long form. They publish every port listed in `EXPOSE` instructions to random host ports. Use `docker port <container>` to see the mapping.

> [!question] 14. Which command would you use to run a one-off database migration in Compose?
> a) `docker compose exec backend python manage.py migrate`
> b) `docker compose run --rm backend python manage.py migrate`
> c) `docker compose up backend migrate`
> d) `docker compose start migrate`
>> [!success]- Answer
>> **b) `docker compose run --rm backend python manage.py migrate`.**
>> `run` creates a new container with the service's config (but does not start the service itself). `--rm` removes the container after the command finishes. `exec` would run the command in the **already-running** backend container, which may not be what you want for a one-off migration.

> [!question] 15. Which capability allows a container to bind to ports below 1024?
> a) `CAP_NET_ADMIN`
> b) `CAP_NET_BIND_SERVICE`
> c) `CAP_SYS_ADMIN`
> d) `CAP_NET_RAW`
>> [!success]- Answer
>> **b) `CAP_NET_BIND_SERVICE`.**
>> By default, only root can bind to ports below 1024 (the "privileged ports"). The `CAP_NET_BIND_SERVICE` capability grants this privilege specifically. To run a non-root container that binds to port 80: `docker run --user 1000 --cap-add=NET_BIND_SERVICE nginx`.

> [!question] 16. Which `docker run` flag sets the hard memory limit?
> a) `--memory-swap`
> b) `--memory-reservation`
> c) `--memory` (or `-m`)
> d) `--memory-swappiness`
>> [!success]- Answer
>> **c) `--memory` (or `-m`).**
>> `--memory` is the hard limit; the container cannot exceed it. `--memory-reservation` is a soft limit (a hint to the kernel under memory pressure). `--memory-swap` is the total memory + swap limit. `--memory-swappiness` controls how willing the kernel is to swap.

> [!question] 17. What does the `condition: service_healthy` in `depends_on` do?
> a) Restarts the service if it becomes unhealthy
> b) Waits for the dependency's healthcheck to pass before starting this service
> c) Sets the service's healthcheck policy
> d) Disables the service's healthcheck
>> [!success]- Answer
>> **b) Waits for the dependency's healthcheck to pass before starting this service.**
>> This is the proper way to wait for a database to be **ready** (not just started) before starting the backend. Combine with a `healthcheck` on the dependency:
>> ```yaml
>> depends_on:
>>   db:
>>     condition: service_healthy
>> ```

> [!question] 18. Which Docker Compose command validates and prints the final YAML after variable substitution?
> a) `docker compose validate`
> b) `docker compose lint`
> c) `docker compose config`
> d) `docker compose inspect`
>> [!success]- Answer
>> **c) `docker compose config`.**
>> `config` parses the compose file(s), substitutes variables, merges multiple files (if `-f` is used), and prints the resulting YAML. Useful for debugging "why is my variable not being substituted?"

> [!question] 19. Which network driver would you use for a container that processes untrusted files and should have no network access?
> a) `bridge`
> b) `host`
> c) `none`
> d) `overlay`
>> [!success]- Answer
>> **c) `none`.**
>> The `none` driver gives the container only a loopback interface. It cannot reach the network, and the network cannot reach it (except via `docker exec`). Perfect for sandboxed file processing.

> [!question] 20. Which Docker feature lets you mount a secret as a file in `/run/secrets/` (typically tmpfs)?
> a) `--env-file`
> b) Docker secrets (Swarm) or Compose secrets (V2)
> c) `ENV` instruction in Dockerfile
> d) `ARG` in Dockerfile
>> [!success]- Answer
>> **b) Docker secrets (Swarm) or Compose secrets (V2).**
>> Secrets are mounted as files at `/run/secrets/<name>`, in tmpfs (RAM) — never written to disk. They are more secure than environment variables (which are visible in `docker inspect` and `/proc/<pid>/environ`).

---

## Section C — Matching

> [!question] 21. Match each network driver with its primary use case.
>
>> [!example] Group A
>> a) `bridge` (default)
>> b) User-defined `bridge`
>> c) `host`
>> d) `none`
>> e) `overlay`
>> f) `macvlan`
>>
>> [!example] Group B
>> n) Multi-host networking across a Swarm cluster
>> o) Container shares the host's network stack — no isolation
>> p) Default for single containers; no DNS
>> q) Container appears as a separate physical device on the LAN
>> r) Custom bridge with DNS service discovery
>> s) No networking at all (loopback only)
>
>> [!success]- Answer
>> a) `bridge` (default) → **p)** Default for single containers; no DNS.
>> b) User-defined `bridge` → **r)** Custom bridge with DNS service discovery.
>> c) `host` → **o)** Container shares the host's network stack — no isolation.
>> d) `none` → **s)** No networking at all (loopback only).
>> e) `overlay` → **n)** Multi-host networking across a Swarm cluster.
>> f) `macvlan` → **q)** Container appears as a separate physical device on the LAN.

---

## Section D — Scenario-Based

> [!question] 22. You have a backend container that cannot connect to a database container. Both are running. The backend logs show "Could not resolve host: db." What are the most likely causes?
>> [!success]- Answer
>> **Cause 1: Containers are on different networks**
>> If the backend is on `app-net` and the db is on `db-net`, they cannot resolve each other. Check with `docker network inspect app-net` and `docker network inspect db-net` — both containers must be listed on the same network.
>>
>> **Cause 2: One or both containers are on the default `bridge`**
>> The default `bridge` does not provide DNS. Move them to a user-defined bridge:
>> ```bash
>> docker network create my-net
>> docker run -d --name db --network my-net postgres
>> docker run -d --name app --network my-net myapp
>> ```
>>
>> **Cause 3: The db container is named something else**
>> DNS resolution is by **container name** (or network alias), not by image name. If you started the db with `--name postgres`, the backend must connect to `postgres`, not `db`.
>>
>> **Cause 4: DNS cache in the backend app**
>> Some apps (especially Java apps) cache DNS results forever. If the db container was recreated (new IP), the backend may still be using the old IP. Restart the backend or configure shorter DNS TTL.
>>
>> **Diagnosis commands**:
>> ```bash
>> docker exec backend cat /etc/resolv.conf    # should show nameserver 127.0.0.11
>> docker exec backend nslookup db             # can it resolve?
>> docker exec backend ping -c1 db             # can it reach the IP?
>> docker network inspect <network>            # are both containers listed?
>> ```

> [!question] 23. Your Docker Compose stack has `frontend`, `backend`, and `db` services. The frontend should NOT be able to reach the db directly. How do you design the networks?
>> [!success]- Answer
>> Use two separate networks:
>>
>> ```yaml
>> services:
>>   db:
>>     image: postgres:15
>>     networks: [back-net]
>>
>>   backend:
>>     build: ./backend
>>     networks: [front-net, back-net]
>>     depends_on: [db]
>>
>>   frontend:
>>     build: ./frontend
>>     networks: [front-net]
>>     depends_on: [backend]
>>
>> networks:
>>   front-net:
>>   back-net:
>> ```
>>
>> Now:
>> - `frontend` is on `front-net` only. It can reach `backend` (also on `front-net`) but **not** `db`.
>> - `backend` is on both networks. It can reach `db` (on `back-net`) and be reached by `frontend` (on `front-net`).
>> - `db` is on `back-net` only. Only `backend` can reach it.
>>
>> This is the multi-tier network isolation pattern. It prevents a compromised frontend from directly attacking the database.

> [!question] 24. A container is consuming all CPU on the host. How do you limit it, and how do you verify the limit is working?
>> [!success]- Answer
>> **Limit CPU at runtime**:
>> ```bash
>> docker run -d --cpus=1.5 --memory=1g myapp
>> ```
>> `--cpus=1.5` means the container can use at most 1.5 CPU cores per scheduling period.
>>
>> **Verify**:
>> ```bash
>> # Watch live CPU usage
>> docker stats <container>
>>
>> # Check the cgroup limit from inside the container
>> docker exec <container> cat /sys/fs/cgroup/cpu.max
>> # Output (cgroup v2): 150000 100000
>> # means quota=150ms, period=100ms, i.e., 1.5 CPUs
>> ```
>>
>> You can also update the limit on a running container:
>> ```bash
>> docker update --cpus=2 <container>
>> ```
>>
>> Note that CPU throttling is **silent** — the container runs slower, not crashes. If your app's latency spikes, check `docker stats` for CPU usage near the limit.

> [!question] 25. Why is it a security risk to run a container as root, and what are two ways to avoid it?
>> [!success]- Answer
>> **Why it is a risk**:
>> By default, containers run as root (UID 0). Without user namespace remapping, UID 0 inside the container is the same as UID 0 on the host. If an attacker exploits a vulnerability in your application and escapes the container (via a kernel exploit, for example), they have root on the host. They can read all files, install malware, attack other containers, and pivot to other services.
>>
>> **Way 1: Create a non-root user in the Dockerfile**
>> ```dockerfile
>> FROM node:18-alpine
>> RUN addgroup -S app && adduser -S app -G app
>> WORKDIR /app
>> COPY --chown=app:app . .
>> USER app
>> CMD ["node", "server.js"]
>> ```
>>
>> **Way 2: Use `--user` at runtime**
>> ```bash
>> docker run --user 1000:1000 myapp
>> # or use the host user's UID/GID:
>> docker run --user $(id -u):$(id -g) myapp
>> ```
>>
>> **Bonus: Use distroless images** that ship without a shell and run as non-root by default. This reduces the attack surface (no shell for an attacker to use).

---

## Section E — Fill in the Blank

> [!question] 26. The Docker Compose command to start services in the background is **__________**.
>> [!success]- Answer
>> `docker compose up -d` (or `docker-compose up -d` in V1).
>> The `-d` (detached) flag runs the services in the background and returns your terminal.

> [!question] 27. The Linux kernel feature that limits a container's CPU and memory consumption is called **__________**.
>> [!success]- Answer
>> **cgroups** (control groups).
>> Cgroups are the kernel's resource accounting and enforcement mechanism. Docker exposes them via `docker run --cpus` and `--memory` flags.

> [!question] 28. To resolve a service named `redis` from inside another container in Docker Compose, you connect to **__________**.
>> [!success]- Answer
>> `redis` (the service name).
>> Compose creates a user-defined bridge network and provides DNS by service name. Your app connects with `host=redis` (not `localhost` or an IP).

> [!question] 29. The `--cap-drop=ALL --cap-add=NET_BIND_SERVICE` flags drop all Linux capabilities and add back only the one needed to **__________**.
>> [!success]- Answer
>> Bind to ports below 1024 (privileged ports).
>> `CAP_NET_BIND_SERVICE` grants this privilege. Dropping all capabilities and adding back only what you need is the secure alternative to `--privileged`.

> [!question] 30. The Docker CLI command to display live resource usage (CPU, memory, network I/O) for all running containers is **__________**.
>> [!success]- Answer
>> `docker stats`.
>> Add a container name to see just one: `docker stats web`. Add `--no-stream` for a single snapshot.

---

Related: [[5. Container Lifecycle and Management]] | [[6. Docker Networking]] | [[7. Docker Compose]] | [[8. Docker Security]] | [[Quiz 2 - Dockerfile and Volumes]]

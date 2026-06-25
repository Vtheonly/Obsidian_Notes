# Quiz 1 - Containers and Virtualization

> [!info] About This Quiz
> This quiz covers the foundational concepts from [[1. What is Docker]], [[1.1 Container Isolation Internals]], and [[2. Installing Docker]]. For each question, the answer is hidden in a callout — try to answer first, then reveal.

Related: [[1. What is Docker]] | [[1.1 Container Isolation Internals]] | [[2. Installing Docker]]

---

## Section A — True or False

> [!question] 1. A container runs its own complete, independent operating system, including its own OS kernel.
>> [!success]- Answer
>> **False.**
>> Containers **share the host's OS kernel**. They do not boot their own kernel. This is the fundamental architectural difference between containers and virtual machines. A container is just an ordinary Linux process (or group of processes) placed inside kernel **namespaces** (for visibility isolation) and assigned to a **cgroup** (for resource limits). The kernel is provided by the host; the container only carries the userspace libraries and binaries it needs.

> [!question] 2. The "Works on My Machine" problem is primarily caused by inconsistencies between development, testing, and production environments.
>> [!success]- Answer
>> **True.**
>> Environment drift — different OS versions, runtime versions, library versions, configuration files, environment variables — is exactly the problem Docker containers solve. By packaging the application together with all of its dependencies and configuration, a container guarantees that the application behaves the same way regardless of where it runs.

> [!question] 3. The only prerequisite needed on a computer to run a containerized application is the Docker platform itself.
>> [!success]- Answer
>> **True** (with a caveat).
>> Docker is the sole requirement on the host: the container brings its own runtime, dependencies, and code. The caveat is that Docker itself requires a Linux kernel — on macOS and Windows, Docker Desktop provides a hidden Linux VM (HyperKit on Mac, WSL 2 on Windows) to satisfy this requirement.

> [!question] 4. Virtual Machines (VMs) are generally more lightweight and faster to start than containers.
>> [!success]- Answer
>> **False.**
>> VMs are heavier and slower to start because each VM boots a full guest OS kernel. Containers start in milliseconds because they do not boot a kernel — they just start a process in an existing kernel. A VM might take 30 seconds to boot; a container typically starts in under a second.

> [!question] 5. Docker containers on a single host machine share the host's operating system kernel.
>> [!success]- Answer
>> **True.**
>> This is the defining architectural property of containers. All containers on a host share the same kernel; isolation is provided by namespaces (PID, NET, MNT, IPC, UTS, USER) and cgroups, not by separate kernels.

> [!question] 6. Using containers complicates the setup process for developers joining a new project.
>> [!success]- Answer
>> **False.**
>> Containers **simplify** setup. A new developer only needs to install Docker; the rest of the environment (runtime, dependencies, configuration) comes inside the container. Without containers, onboarding might involve a multi-page setup guide and hours of installing specific versions of Node.js, Python, etc.

> [!question] 7. A container packages an application's source code, but not its dependencies or runtime.
>> [!success]- Answer
>> **False.**
>> A container bundles **everything** the application needs to run: source code, dependencies (e.g., `node_modules`, `site-packages`), the runtime (Node.js, Python), system libraries (`libssl`, `glibc`), and configuration files. This is the entire point — the container is a self-contained, portable unit.

> [!question] 8. The consistency provided by containers is beneficial for development but not for deploying applications to production servers.
>> [!success]- Answer
>> **False.**
>> Container consistency is arguably **more** valuable in production than in development. In production, you want deployments to be reproducible, predictable, and free of "works in staging but not in prod" issues. The same image that was tested in staging is deployed to production — guaranteeing identical behavior.

> [!question] 9. One of the main benefits of using containers is application isolation, which prevents conflicts between different projects' requirements.
>> [!success]- Answer
>> **True.**
>> Each container has its own isolated filesystem, network, and process tree (via namespaces). Two containers can run conflicting versions of the same library without affecting each other. Project A's container can run Node 16 while Project B's container runs Node 18, on the same host, with no conflict.

> [!question] 10. Containers consume significantly fewer resources than VMs, allowing more applications to run on a single host.
>> [!success]- Answer
>> **True.**
>> Containers do not include a full guest OS, so they consume far less CPU, memory, and disk. A host that can run 5 VMs might run 50 or 100 containers. This density is why cloud providers can pack many customer workloads onto shared infrastructure (e.g., AWS Fargate tasks share an EC2 instance).

---

## Section B — Multiple Choice

> [!question] 11. What is the primary problem that Docker and containers aim to solve?
> a) Slow internet connections
> b) Writing application source code
> c) The "Works on My Machine" issue due to environment inconsistency
> d) The lack of programming languages
>> [!success]- Answer
>> **c) The "Works on My Machine" issue due to environment inconsistency.**
>> Docker solves environment drift by packaging the application with all its dependencies into a single, immutable image. The image runs identically on any host with Docker installed. The other options are not problems Docker addresses.

> [!question] 12. Which of the following best describes a Docker container?
> a) A heavyweight virtual machine with its own OS
> b) A server for hosting websites
> c) A standardized, self-contained package that bundles an application and all its dependencies
> d) A tool for compiling source code
>> [!success]- Answer
>> **c) A standardized, self-contained package that bundles an application and all its dependencies.**
>> A container is a running instance of an image. It includes the application's code, runtime, libraries, and configuration. It is **not** a VM (no separate kernel), not a server (it is one process), and not a compiler (it runs already-compiled code).

> [!question] 13. What is the key architectural difference between a container and a Virtual Machine (VM)?
> a) Containers can only run on Linux, while VMs can run on any OS.
> b) Containers share the host machine's OS kernel, while VMs have their own full guest OS.
> c) VMs are used for development, while containers are only for production.
> d) VMs cannot run application code directly.
>> [!success]- Answer
>> **b) Containers share the host machine's OS kernel, while VMs have their own full guest OS.**
>> A VM virtualizes the **hardware** and runs a complete guest OS (with its own kernel) on top of a hypervisor. A container virtualizes the **OS** — it shares the host kernel and is just an isolated process. This is why containers are lighter and faster than VMs.
>
> Note about option (a): Linux containers require a Linux kernel. On macOS/Windows, Docker Desktop runs a hidden Linux VM to provide that kernel. Windows containers (rare) require a Windows kernel. So technically, containers are tied to the kernel they were built for, but it is not "Linux only" — Windows containers exist.

> [!question] 14. Why are containers considered "lightweight" compared to VMs?
> a) They use a more efficient programming language.
> b) They compress the application's source code.
> c) They do not need to boot an entire operating system.
> d) They require more powerful hardware to run.
>> [!success]- Answer
>> **c) They do not need to boot an entire operating system.**
>> A container starts as a regular Linux process — no kernel boot, no init system, no full OS userspace. A VM must boot an entire OS kernel, which takes seconds to minutes and consumes hundreds of MB of RAM. Containers start in milliseconds and use only what their application needs.

> [!question] 15. Which of the following is NOT typically included inside a container?
> a) The application's source code
> b) A full, independent OS kernel
> c) The specific runtime version required (e.g., Node.js)
> d) Application dependencies and libraries
>> [!success]- Answer
>> **b) A full, independent OS kernel.**
>> A container **shares** the host's kernel. It does not include its own kernel. The container's filesystem contains userspace libraries (glibc/musl, libssl, etc.) and the application's runtime and code, but not the kernel itself.

> [!question] 16. What does running an application in "isolation" mean in the context of Docker?
> a) The application cannot access the internet.
> b) The application's environment is separate from the host machine and other containers.
> c) Only one user can access the application at a time.
> d) The application runs on a physically separate machine.
>> [!success]- Answer
>> **b) The application's environment is separate from the host machine and other containers.**
>> Isolation in Docker means the container has its own filesystem view (via overlay2), its own network stack (via NET namespace), its own process list (via PID namespace), and so on. The container does not see host processes, host files (except where mounted), or other containers' resources.

> [!question] 17. What is the core function of the Docker platform?
> a) To provide an online code editor
> b) To manage user authentication
> c) To design database schemas
> d) To build, share, and run containers
>> [!success]- Answer
>> **d) To build, share, and run containers.**
>> Docker is a platform and toolset for the entire container lifecycle: building images (via `docker build` and Dockerfiles), sharing them (via Docker Hub and other registries), and running them (via `docker run`).

> [!question] 18. According to the text, when would a Virtual Machine be a more suitable choice than a container?
> a) When efficiency and speed are the top priorities.
> b) When you need to run a completely different OS than the host (e.g., Windows on a Linux host).
> c) When deploying a simple web application.
> d) When you want to minimize resource consumption.
>> [!success]- Answer
>> **b) When you need to run a completely different OS than the host (e.g., Windows on a Linux host).**
>> Containers require the host's kernel. A Linux container cannot run on a Windows host directly (you would need a Linux VM underneath). VMs virtualize the hardware, so a Windows VM can run on a Linux host and vice versa. For most application deployment, containers are preferred; VMs are used when full-OS isolation or cross-OS support is required.

> [!question] 19. What are "dependencies" in the context of a software project?
> a) The developers who work on the project.
> b) The servers where the application is deployed.
> c) The project's budget and timeline.
> d) The collection of libraries, runtimes, and tools the application needs to function.
>> [!success]- Answer
>> **d) The collection of libraries, runtimes, and tools the application needs to function.**
>> Dependencies include language libraries (npm packages, pip packages), system libraries (libssl, libcurl), language runtimes (Node.js, Python), and build tools. Containers bundle all of these so the host does not need to provide them.

> [!question] 20. How does using Docker for development benefit the deployment to production?
> a) It makes the production server run faster.
> b) It eliminates the need for a production server.
> c) It ensures consistency, as the same container tested in development can be deployed to production.
> d) It automatically scales the application based on traffic.
>> [!success]- Answer
>> **c) It ensures consistency, as the same container tested in development can be deployed to production.**
>> Docker's core promise: the image is the deployable artifact. Test the same image in staging, deploy the same image to production. The behavior is identical because the image is immutable. This eliminates "works in staging, broken in prod" issues caused by environment differences.

---

## Section C — Matching

> [!question] 21. Match each Docker-related term with its correct description.
>
>> [!example] Group A
>> a) Container
>> b) Virtual Machine (VM)
>> c) Isolation
>> d) Dependencies
>> e) Docker
>> f) Consistency
>> g) Host Machine
>> h) OS Kernel
>> i) Lightweight
>> j) "Works on my machine"
>>
>> [!example] Group B
>> n) The central component of an operating system that containers share from the host.
>> o) A problem stemming from environmental differences between machines.
>> p) Ensures an application behaves the same way regardless of where it is run.
>> q) The physical or virtual computer on which Docker is installed and containers are run.
>> r) A characteristic of containers, as they don't include a full OS.
>> s) A platform and toolset for building, sharing, and running containerized applications.
>> t) A self-contained, runnable package including an application, its runtime, and configurations.
>> u) An environment that runs a complete, independent operating system.
>> v) The principle of keeping a container's processes separate from the host and other containers.
>> w) External libraries, packages, and runtimes required by an application to run.
>
>> [!success]- Answer
>> a) Container → **t)** A self-contained, runnable package including an application, its runtime, and configurations.
>> b) Virtual Machine → **u)** An environment that runs a complete, independent operating system.
>> c) Isolation → **v)** The principle of keeping a container's processes separate from the host and other containers.
>> d) Dependencies → **w)** External libraries, packages, and runtimes required by an application to run.
>> e) Docker → **s)** A platform and toolset for building, sharing, and running containerized applications.
>> f) Consistency → **p)** Ensures an application behaves the same way regardless of where it is run.
>> g) Host Machine → **q)** The physical or virtual computer on which Docker is installed and containers are run.
>> h) OS Kernel → **n)** The central component of an operating system that containers share from the host.
>> i) Lightweight → **r)** A characteristic of containers, as they don't include a full OS.
>> j) "Works on my machine" → **o)** A problem stemming from environmental differences between machines.

---

## Section D — Deep Conceptual Questions

> [!question] 22. Explain in your own words why a Linux container cannot run natively on a macOS host without Docker Desktop's hidden Linux VM.
>> [!success]- Answer
>> A Linux container is, at its core, a Linux process isolated by Linux kernel features (namespaces, cgroups, overlay2). These features exist only in the Linux kernel. macOS uses a different kernel called XNU (a hybrid of Mach and BSD); it does not implement Linux namespaces or cgroups.
>>
>> Therefore, to run a Linux container on macOS, Docker Desktop runs a lightweight Linux VM (via HyperKit on Intel Macs, Apple Virtualization Framework on Apple Silicon). The Docker daemon runs inside this VM, talking directly to the Linux kernel inside the VM. The `docker` CLI on macOS connects to the daemon inside the VM.
>>
>> Without this VM, the macOS kernel cannot provide the isolation primitives a Linux container needs.

> [!question] 23. Why is `--privileged` considered dangerous, and what is the recommended alternative?
>> [!success]- Answer
>> `--privileged` disables almost all of Docker's isolation:
>> - It grants **all** Linux capabilities (instead of dropping dangerous ones).
>> - It disables **seccomp** filtering (so all syscalls are allowed).
>> - It gives the container access to **all host devices** (e.g., `/dev/sda`).
>> - It turns off **AppArmor** protection.
>>
>> A privileged container can typically escape to the host in seconds — for example, by mounting the host's root filesystem and writing an SSH key to `/root/.ssh/authorized_keys`.
>>
>> **Recommended alternative**: Drop all capabilities and add back only the specific ones your app needs:
>> ```bash
>> docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE myapp
>> ```
>> If you genuinely need device access, mount only that specific device with `--device=/dev/xxx`.

> [!question] 24. A container exits with code 137. What is the most likely cause, and how do you confirm it?
>> [!success]- Answer
>> Exit code 137 = 128 + 9, which means the process was killed by **signal 9 (SIGKILL)**. The most common cause is the kernel's **OOM killer** terminating the process because the container exceeded its memory limit.
>>
>> To confirm:
>> ```bash
>> docker inspect <container> --format '{{.State.OOMKilled}}'
>> # true means the kernel OOM-killed the container
>>
>> docker inspect <container> --format '{{.State.ExitCode}}'
>> # 137
>> ```
>>
>> Also check `docker logs <container>` for any "Cannot allocate memory" or "Out of memory" messages.
>>
>> Fixes:
>> - Increase `--memory` in `docker run` or `mem_limit` in Compose.
>> - Profile the app to find the memory leak (e.g., `node --inspect`, `py-spy dump`).
>> - If the limit is correct but the app needs more, optimize the app.

> [!question] 25. You run `docker run -d --name web -p 80:80 nginx` and immediately get "port is already allocated." How do you find what is using port 80?
>> [!success]- Answer
>> ```bash
>> # Linux/macOS: find what is using port 80
>> sudo lsof -i :80
>> sudo ss -tlnp | grep :80
>> sudo netstat -tlnp | grep :80
>>
>> # Check if another Docker container has it
>> docker ps --format "table {{.Names}}\t{{.Ports}}" | grep :80
>> ```
>>
>> Common culprits:
>> - Another Docker container already bound to host port 80.
>> - A locally-installed Nginx/Apache running on the host.
>> - On macOS: a system process (rare, since macOS uses port 80 for some services).
>>
>> Solutions:
>> - Stop the conflicting process: `sudo systemctl stop nginx` or `docker stop <other-container>`.
>> - Use a different host port: `-p 8080:80`.

---

## Section E — Fill in the Blank

> [!question] 26. The three kernel features that together implement container isolation are **__________**, **__________**, and **__________**.
>> [!success]- Answer
>> **Namespaces**, **cgroups** (control groups), and **union filesystems** (specifically overlay2).
>> - **Namespaces** limit what a process can see (PID, NET, MNT, IPC, UTS, USER).
>> - **Cgroups** limit what a process can use (CPU, memory, I/O, PIDs).
>> - **Union filesystems** (overlay2) compose the container's view of its filesystem from read-only image layers plus a writable container layer.

> [!question] 27. The two `docker run` flags you should always use together for an interactive shell inside a running container are **__________** and **__________**.
>> [!success]- Answer
>> `-i` and `-t` (commonly written as `-it`).
>> - `-i` keeps STDIN open so the container can receive your keyboard input.
>> - `-t` allocates a pseudo-TTY so the shell has proper terminal formatting (colors, cursor, tab completion).

> [!question] 28. The Docker CLI command that lists **all** containers (running and stopped) is **__________**.
>> [!success]- Answer
>> `docker ps -a` (or `docker ps --all`).
>> Without `-a`, `docker ps` shows only running containers.

> [!question] 29. The Dockerfile instruction that runs a command **at build time** to install dependencies is **__________**, while the instruction that specifies the command to run **when the container starts** is **__________**.
>> [!success]- Answer
>> `RUN` (build time) and `CMD` (run time).
>> - `RUN npm install` runs once during `docker build` and the result is baked into the image.
>> - `CMD ["node", "server.js"]` runs every time a container is started from the image.

> [!question] 30. In a Docker Compose file, services communicate with each other using **__________** as the hostname, not IP addresses.
>> [!success]- Answer
>> The **service name**.
>> Docker Compose creates a user-defined bridge network for the project and provides DNS resolution by service name. If your compose file has a service called `db`, other services can connect to it as `db` (e.g., `host=db` in your config).

---

Related: [[1. What is Docker]] | [[1.1 Container Isolation Internals]] | [[2. Installing Docker]] | [[Quiz 2 - Dockerfile and Volumes]]

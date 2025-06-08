---
sources:
  - "[[Understanding Docker: The Fundamentals]]"
---
> [!question] A container runs its own complete, independent operating system, including its own OS kernel.
>> [!success]- Answer
>> False

> [!question] The "Works on My Machine" problem is primarily caused by inconsistencies between development, testing, and production environments.
>> [!success]- Answer
>> True

> [!question] The only prerequisite needed on a computer to run a containerized application is the Docker platform itself.
>> [!success]- Answer
>> True

> [!question] Virtual Machines (VMs) are generally more lightweight and faster to start than containers.
>> [!success]- Answer
>> False

> [!question] Docker containers on a single host machine share the host's operating system kernel.
>> [!success]- Answer
>> True

> [!question] Using containers complicates the setup process for developers joining a new project.
>> [!success]- Answer
>> False

> [!question] A container packages an application's source code, but not its dependencies or runtime.
>> [!success]- Answer
>> False

> [!question] The consistency provided by containers is beneficial for development but not for deploying applications to production servers.
>> [!success]- Answer
>> False

> [!question] One of the main benefits of using containers is application isolation, which prevents conflicts between different projects' requirements.
>> [!success]- Answer
>> True

> [!question] Containers consume significantly fewer resources than VMs, allowing more applications to run on a single host.
>> [!success]- Answer
>> True

> [!question] What is the primary problem that Docker and containers aim to solve?
> a) Slow internet connections
> b) Writing application source code
> c) The "Works on My Machine" issue due to environment inconsistency
> d) The lack of programming languages
>> [!success]- Answer
>> c) The "Works on My Machine" issue due to environment inconsistency

> [!question] Which of the following best describes a Docker container?
> a) A heavyweight virtual machine with its own OS
> b) A server for hosting websites
> c) A standardized, self-contained package that bundles an application and all its dependencies
> d) A tool for compiling source code
>> [!success]- Answer
>> c) A standardized, self-contained package that bundles an application and all its dependencies

> [!question] What is the key architectural difference between a container and a Virtual Machine (VM)?
> a) Containers can only run on Linux, while VMs can run on any OS.
> b) Containers share the host machine's OS kernel, while VMs have their own full guest OS.
> c) VMs are used for development, while containers are only for production.
> d) VMs cannot run application code directly.
>> [!success]- Answer
>> b) Containers share the host machine's OS kernel, while VMs have their own full guest OS.

> [!question] Why are containers considered "lightweight" compared to VMs?
> a) They use a more efficient programming language.
> b) They compress the application's source code.
> c) They do not need to boot an entire operating system.
> d) They require more powerful hardware to run.
>> [!success]- Answer
>> c) They do not need to boot an entire operating system.

> [!question] Which of the following is NOT typically included inside a container?
> a) The application's source code
> b) A full, independent OS kernel
> c) The specific runtime version required (e.g., Node.js)
> d) Application dependencies and libraries
>> [!success]- Answer
>> b) A full, independent OS kernel

> [!question] What does running an application in "isolation" mean in the context of Docker?
> a) The application cannot access the internet.
> b) The application's environment is separate from the host machine and other containers.
> c) Only one user can access the application at a time.
> d) The application runs on a physically separate machine.
>> [!success]- Answer
>> b) The application's environment is separate from the host machine and other containers.

> [!question] What is the core function of the Docker platform?
> a) To provide an online code editor
> b) To manage user authentication
> c) To design database schemas
> d) To build, share, and run containers
>> [!success]- Answer
>> d) To build, share, and run containers

> [!question] According to the text, when would a Virtual Machine be a more suitable choice than a container?
> a) When efficiency and speed are the top priorities.
> b) When you need to run a completely different OS than the host (e.g., Windows on a Linux host).
> c) When deploying a simple web application.
> d) When you want to minimize resource consumption.
>> [!success]- Answer
>> b) When you need to run a completely different OS than the host (e.g., Windows on a Linux host).

> [!question] What are "dependencies" in the context of a software project?
> a) The developers who work on the project.
> b) The servers where the application is deployed.
> c) The project's budget and timeline.
> d) The collection of libraries, runtimes, and tools the application needs to function.
>> [!success]- Answer
>> d) The collection of libraries, runtimes, and tools the application needs to function.

> [!question] How does using Docker for development benefit the deployment to production?
> a) It makes the production server run faster.
> b) It eliminates the need for a production server.
> c) It ensures consistency, as the same container tested in development can be deployed to production.
> d) It automatically scales the application based on traffic.
>> [!success]- Answer
>> c) It ensures consistency, as the same container tested in development can be deployed to production.

> [!question] Match the Docker-related term with its correct description.
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
>
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
>> a) -> t)
>> b) -> u)
>> c) -> v)
>> d) -> w)
>> e) -> s)
>> f) -> p)
>> g) -> q)
>> h) -> n)
>> i) -> r)
>> j) -> o)
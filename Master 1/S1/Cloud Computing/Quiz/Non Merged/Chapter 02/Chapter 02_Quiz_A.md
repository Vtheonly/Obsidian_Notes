---
sources:
  - "[[Chapter 2 - Service and Deployment Models/2.1 Hierarchical Cloud Infrastructure and Architecture.md]]"
  - "[[Chapter 2 - Service and Deployment Models/2.2 Cloud Service Models - IaaS PaaS SaaS Deep Dive.md]]"
  - "[[Chapter 2 - Service and Deployment Models/2.3 The Shared Responsibility Model.md]]"
  - "[[Chapter 2 - Service and Deployment Models/2.4 Cloud Deployment Models - Public Private Hybrid Community.md]]"
  - "[[Chapter 2 - Service and Deployment Models/2.5 Cloud Architecture Layers and Responsibility Boundaries.md]]"
  - "[[Chapter 2 - Service and Deployment Models/2.6 Cloud Deployment Architectures and Network Trade-offs.md]]"
  - "[[Chapter 2 - Service and Deployment Models/2.7 What is VPS and EC2.md]]"
  - "[[Chapter 2 - Service and Deployment Models/2.8 What is a VPC.md]]"
---

> [!question] IaaS provides users with virtual machines, storage, and networking resources.
>> [!success]- Answer
>> True

> [!question] In PaaS, the user manages the operating system and middleware.
>> [!success]- Answer
>> False

> [!question] SaaS delivers ready-to-use software applications over the internet.
>> [!success]- Answer
>> True

> [!question] The Shared Responsibility Model means the provider is responsible for everything.
>> [!success]- Answer
>> False

> [!question] A public cloud is deployed for exclusive use by a single organization.
>> [!success]- Answer
>> False

> [!question] A private cloud can be hosted on-premises or by a third-party provider.
>> [!success]- Answer
>> True

> [!question] A hybrid cloud combines public and private cloud infrastructures.
>> [!success]- Answer
>> True

> [!question] A VPC is a physically isolated section of a cloud provider's network.
>> [!success]- Answer
>> False

> [!question] In the IaaS model, the user has full control over the operating system.
>> [!success]- Answer
>> True

> [!question] A community cloud is shared by several organizations with common concerns.
>> [!success]- Answer
>> True

> [!question] Which cloud service model provides the highest level of user control?
> a) SaaS
> b) PaaS
> c) IaaS
> d) FaaS
>> [!success]- Answer
>> c) IaaS

> [!question] In the Shared Responsibility Model, who is responsible for physical security?
> a) The customer
> b) The cloud provider
> c) Both equally
> d) A third-party auditor
>> [!success]- Answer
>> b) The cloud provider

> [!question] Which deployment model offers the best balance of cost and control?
> a) Public cloud only
> b) Private cloud only
> c) Hybrid cloud
> d) Community cloud
>> [!success]- Answer
>> c) Hybrid cloud

> [!question] What does VPC stand for?
> a) Virtual Private Cloud
> b) Virtual Public Connection
> c) Verified Private Channel
> d) Variable Protocol Configuration
>> [!success]- Answer
>> a) Virtual Private Cloud

> [!question] Which service model abstracts the most infrastructure from the user?
> a) IaaS
> b) PaaS
> c) SaaS
> d) All equally
>> [!success]- Answer
>> c) SaaS

> [!question] What is the primary benefit of PaaS for developers?
> a) Full control over hardware
> b) Reduced management of underlying infrastructure
> c) Lower network latency
> d) Physical server access
>> [!success]- Answer
>> b) Reduced management of underlying infrastructure

> [!question] Which statement about the frontend of cloud architecture is correct?
> a) It manages backend storage
> b) It includes the client interface like browsers and CLIs
> c) It handles physical security
> d) It manages hypervisors
>> [!success]- Answer
>> b) It includes the client interface like browsers and CLIs

> [!question] What is the role of a load balancer in cloud architecture?
> a) Store database records
> b) Distribute incoming traffic across servers
> c) Compile application code
> d) Manage user authentication
>> [!success]- Answer
>> b) Distribute incoming traffic across servers

> [!question] Which of the following is an example of SaaS?
> a) Amazon EC2
> b) Google App Engine
> c) Microsoft Office 365
> d) OpenStack
>> [!success]- Answer
>> c) Microsoft Office 365

> [!question] What does the backend of cloud architecture include?
> a) Only the user's browser
> b) Application layer, service layer, and physical infrastructure
> c) Just network cables
> d) Only client applications
>> [!success]- Answer
>> b) Application layer, service layer, and physical infrastructure

> [!question] Match the cloud service model with the level of control.
>> [!example] Group A
>> a) IaaS
>> b) PaaS
>> c) SaaS
>> d) FaaS
>
>> [!example] Group B
>> n) User controls OS, middleware, and applications
>> o) User controls applications and data only
>> p) User only configures usage settings
>> q) User controls function code and triggers
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the deployment model with its access scope.
>> [!example] Group A
>> a) Public cloud
>> b) Private cloud
>> c) Hybrid cloud
>> d) Community cloud
>
>> [!example] Group B
>> n) Open to the general public over the internet
>> o) Exclusive use by a single organization
>> p) Interconnected public and private environments
>> q) Shared by organizations with common goals
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the Shared Responsibility component with the responsible party.
>> [!example] Group A
>> a) Physical hardware security
>> b) Network configuration
>> c) Application code security
>> d) Data encryption at rest
>
>> [!example] Group B
>> n) Cloud provider
>> o) Customer (in IaaS)
>> p) Customer
>> q) Customer
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the cloud architecture component with its function.
>> [!example] Group A
>> a) API Gateway
>> b) Load Balancer
>> c) Hypervisor
>> d) IAM
>
>> [!example] Group B
>> n) Routes and manages API requests
>> o) Distributes traffic across instances
>> p) Manages virtual machines on physical hardware
>> q) Controls user access and permissions
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the IaaS component with its cloud equivalent.
>> [!example] Group A
>> a) Physical server
>> b) Storage array
>> c) Network switch
>> d) Data center
>
>> [!example] Group B
>> n) EC2 instance or virtual machine
>> o) EBS volume or block storage
>> p) Virtual network or subnet
>> q) Availability zone or region
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the service model with its primary user.
>> [!example] Group A
>> a) IaaS
>> b) PaaS
>> c) SaaS
>> d) FaaS
>
>> [!example] Group B
>> n) System administrators and DevOps engineers
>> o) Application developers
>> p) End users and business teams
>> q) Event-driven function developers
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the VPC component with its purpose.
>> [!example] Group A
>> a) Subnet
>> b) Route table
>> c) Security group
>> d) Internet gateway
>
>> [!example] Group B
>> n) Logical partition of IP address range
>> o) Defines traffic routing rules
>> p) Virtual firewall for instances
>> q) Connects VPC to the internet
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the PaaS advantage with its benefit.
>> [!example] Group A
>> a) Built-in middleware
>> b) Auto-scaling
>> c) Managed databases
>> d) CI/CD integration
>
>> [!example] Group B
>> n) Reduces configuration effort for developers
>> o) Handles load-based resource adjustments
>> p) Eliminates database administration tasks
>> q) Streamlines deployment pipelines
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the deployment consideration with its trade-off.
>> [!example] Group A
>> a) Public cloud cost
>> b) Private cloud control
>> c) Hybrid cloud complexity
>> d) Community cloud scope
>
>> [!example] Group B
>> n) Lower upfront cost but less control
>> o) Maximum control but higher cost
>> p) Best features but complex integration
>> q) Shared cost but limited customization
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the client infrastructure with its typical use case.
>> [!example] Group A
>> a) Web browser
>> b) CLI terminal
>> c) Mobile app
>> d) Thick client application
>
>> [!example] Group B
>> n) Accessing SaaS dashboards and portals
>> o) Managing cloud resources via scripts
>> p) Interacting with mobile-optimized services
>> q) Running resource-intensive enterprise software
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

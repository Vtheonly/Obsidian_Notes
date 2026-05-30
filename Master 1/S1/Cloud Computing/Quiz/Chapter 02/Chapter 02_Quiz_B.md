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

> [!question] Hypervisors are a key technology enabling IaaS.
>> [!success]- Answer
>> True

> [!question] In SaaS, the user is responsible for software updates and patches.
>> [!success]- Answer
>> False

> [!question] A private cloud can only be hosted on the customer's premises.
>> [!success]- Answer
>> False

> [!question] VPC allows users to define their own virtual network topology in the cloud.
>> [!success]- Answer
>> True

> [!question] PaaS eliminates the need for developers to manage server hardware.
>> [!success]- Answer
>> True

> [!question] In the Shared Responsibility Model, the customer always handles physical access controls.
>> [!success]- Answer
>> False

> [!question] A hybrid cloud must include at least one public and one private cloud.
>> [!success]- Answer
>> True

> [!question] Community clouds are typically more expensive than public clouds.
>> [!success]- Answer
>> False

> [!question] EC2 is an example of a PaaS offering from AWS.
>> [!success]- Answer
>> False

> [!question] Security groups act as virtual firewalls for cloud instances.
>> [!success]- Answer
>> True

> [!question] Which cloud deployment model is best for organizations with strict regulatory requirements?
> a) Public cloud
> b) Private cloud
> c) Community cloud
> d) All equally
>> [!success]- Answer
>> b) Private cloud

> [!question] What is the main advantage of a hybrid cloud?
> a) Lowest possible cost
> b) Complete isolation from the internet
> c) Flexibility to choose where workloads run
> d) No need for internet connectivity
>> [!success]- Answer
>> c) Flexibility to choose where workloads run

> [!question] Which of the following is managed by the customer in all cloud service models?
> a) Physical network infrastructure
> b) Data and access management
> c) Hypervisor software
> d) Storage array hardware
>> [!success]- Answer
>> b) Data and access management

> [!question] What does a Virtual Private Cloud (VPC) provide?
> a) Physical isolation from other cloud users
> b) Logical isolation within a public cloud
> c) Dedicated servers at the provider's data center
> d) A private internet connection
>> [!success]- Answer
>> b) Logical isolation within a public cloud

> [!question] Which model gives the least flexibility but the most convenience?
> a) IaaS
> b) PaaS
> c) SaaS
> d) All equally
>> [!success]- Answer
>> c) SaaS

> [!question] What is the role of middleware in cloud architecture?
> a) Manage physical cooling systems
> b) Provide services like message queuing and databases
> c) Compile application source code
> d) Encrypt all network traffic
>> [!success]- Answer
>> b) Provide services like message queuing and databases

> [!question] Which statement about security groups is true?
> a) They replace encryption
> b) They control inbound and outbound traffic at the instance level
> c) They manage physical server security
> d) They are only in private clouds
>> [!success]- Answer
>> b) They control inbound and outbound traffic at the instance level

> [!question] In which cloud model does the provider manage the runtime environment?
> a) IaaS
> b) PaaS
> c) On-premise
> d) DAS
>> [!success]- Answer
>> b) PaaS

> [!question] What does a subnet define in a VPC?
> a) A billing category
> b) A range of IP addresses within the VPC
> c) A type of VM
> d) A storage volume type
>> [!success]- Answer
>> b) A range of IP addresses within the VPC

> [!question] Which cloud model keeps sensitive data on-premises while using cloud for less critical workloads?
> a) Public cloud only
> b) Private cloud only
> c) Hybrid cloud
> d) Multi-cloud
>> [!success]- Answer
>> c) Hybrid cloud

> [!question] Match the responsibility with the correct party in IaaS.
>> [!example] Group A
>> a) OS patching
>> b) Application security
>> c) Physical hardware
>> d) Network firewall config
>
>> [!example] Group B
>> n) Customer
>> o) Customer
>> p) Cloud provider
>> q) Customer
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the service model with management scope.
>> [!example] Group A
>> a) IaaS management
>> b) PaaS management
>> c) SaaS management
>> d) On-premise management
>
>> [!example] Group B
>> n) User manages OS and above
>> o) User manages apps and data
>> p) User manages usage only
>> q) Organization manages everything
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the cloud term with its definition.
>> [!example] Group A
>> a) Tenant
>> b) Region
>> c) Availability Zone
>> d) Edge Location
>
>> [!example] Group B
>> n) A single customer or organization
>> o) A geographic area with multiple data centers
>> p) An isolated data center within a region
>> q) A CDN endpoint for content delivery
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the deployment scenario with the best model.
>> [!example] Group A
>> a) Startup with minimal budget
>> b) Bank with strict compliance
>> c) E-commerce with variable traffic
>> d) Government research consortium
>
>> [!example] Group B
>> n) Public cloud
>> o) Private cloud
>> p) Hybrid cloud
>> q) Community cloud
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the PaaS component with its function.
>> [!example] Group A
>> a) Runtime engine
>> b) Database service
>> c) Message queue
>> d) CI/CD pipeline
>
>> [!example] Group B
>> n) Executes application code in managed environment
>> o) Provides managed relational database storage
>> p) Enables asynchronous service communication
>> q) Automates build, test, and deployment
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the cloud term with its real-world analogy.
>> [!example] Group A
>> a) IaaS
>> b) PaaS
>> c) SaaS
>> d) VPC
>
>> [!example] Group B
>> n) Renting an empty apartment
>> o) Renting a furnished apartment with utilities
>> p) Staying at a fully serviced hotel
>> q) Having a private wing in an apartment building
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the VPC networking component with its role.
>> [!example] Group A
>> a) NAT gateway
>> b) VPN connection
>> c) Peering connection
>> d) Direct Connect
>
>> [!example] Group B
>> n) Allows private subnets to access the internet
>> o) Encrypted tunnel from on-premises to cloud
>> p) Connects two VPCs privately
>> q) Dedicated private network link to cloud
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the cloud architecture layer with its example.
>> [!example] Group A
>> a) Client infrastructure
>> b) Application layer
>> c) Service layer
>> d) Physical infrastructure
>
>> [!example] Group B
>> n) Web browser or mobile app
>> o) SaaS application like Gmail
>> p) API gateway and message queues
>> q) Servers, cooling, and power systems
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the security component with its purpose.
>> [!example] Group A
>> a) IAM roles
>> b) Encryption at rest
>> c) Encryption in transit
>> d) Security groups
>
>> [!example] Group B
>> n) Define permissions for cloud resources
>> o) Protects stored data from unauthorized access
>> p) Secures data during network transmission
>> q) Acts as a virtual firewall for traffic control
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the cloud service with its category.
>> [!example] Group A
>> a) AWS Lambda
>> b) Google Compute Engine
>> c) Azure SQL Database
>> d) Salesforce
>
>> [!example] Group B
>> n) FaaS (Function as a Service)
>> o) IaaS (Infrastructure as a Service)
>> p) PaaS (Platform as a Service)
>> q) SaaS (Software as a Service)
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

---
title: "CCBD TP2 – Cloud Architecture Analysis and Design"
authors: ["Name1", "Name2"]
course: "Cloud Computing and Big Data (CCBD)"
file: "CCBD_TP2_Name1_Name2.pdf"
---

# 🧩 Clarification & Objective

**Goal:**  
Analyze and design a **multi-level Cloud architecture** (IaaS → PaaS) suited for a **distributed application**, based on concepts studied in **YAFS**.

The main objectives are:
- To understand the **limitations** of a private Cloud (IaaS),
- To explore and prepare the **migration path** toward PaaS-based systems,
- To demonstrate the role of **Cloud components** in distributed architectures.

---

# 🧠 Part 1 – Conceptual Analysis

## 1.1. Components in YAFS

Below is a description of each key Cloud component modeled in YAFS:

| **Component**            | **Role**                                                                | **Functioning**                                                                            |
| ------------------------ | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| **DataCenter**           | Centralized computing hub that hosts VMs and manages service execution. | Handles infrastructure-level resource allocation, network routing, and latency simulation. |
| **Virtual Machine (VM)** | Logical unit of computation running application tasks.                  | Each VM can simulate different workloads, compute capacities, and failure behaviors.       |
| **Scheduler**            | Responsible for managing how tasks are distributed among resources.     | Decides which VM executes which request based on latency, load, or custom policies.        |
| **Network/Topology**     | Represents the communication layer among nodes.                         | Defines bandwidth, delay, and connectivity between components.                             |
| **Application Modules**  | Logical entities representing distributed services.                     | Each module processes requests and communicates with others through YAFS message routing.  |




---


---

# 🧮 Part 2 – Case Study

## 2.1. Application Scenario

**Chosen Distributed Application:**  
_Example: “EduStream” – a lightweight online education and streaming platform._  
The application includes:
- **Frontend:** React web app (deployed via PaaS)  
- **Backend:** API services (Node.js/Flask) hosted on hybrid Cloud  
- **Database:** PostgreSQL (managed via Cloud SQL service)  
- **Edge Layer (optional):** Local caching nodes for reduced latency  

---

## 2.2. Hybrid Cloud Architecture

**Proposed Layers:**

| **Layer** | **Technology Example** | **Role** |
|------------|------------------------|-----------|
| **IaaS** | AWS EC2 / DigitalOcean Droplets | Host backend microservices and persistent storage |
| **PaaS** | Render / Heroku / GCP App Engine | Deploy stateless frontend and lightweight APIs |
| **Edge/Fog (optional)** | Cloudflare Workers / Raspberry Pi Nodes | Cache static assets and route local traffic |

---

# 🔬 Part 3 – Research on PaaS Solutions

| **PaaS Solution** | **Ease of Deployment** | **Autoscaling** | **Pricing Model** | **Microservice Compatibility** |
|--------------------|------------------------|------------------|-------------------|--------------------------------|
| **Render** | Simple Git-based deployment | Yes | Pay-per-resource | Yes |
| **Heroku** | Very easy, abstracted | Limited (dyno-based) | Tiered pricing | Yes |
| **GCP App Engine** | More configuration required | Full autoscaling | Pay-per-use | Strong microservice support |

**Summary:**  
Render offers flexibility and simplicity; Heroku provides developer-friendly tools but limited control; GCP App Engine is best for large-scale distributed systems.

---

# 🏗 Part 4 – Final Architecture Design

## 4.1. Global Architecture Diagram
```mermaid
flowchart LR
    subgraph IaaS["IaaS Layer"]
        VM1[Backend VM]
        DB[(Database Storage)]
    end
    subgraph PaaS["PaaS Layer"]
        Front[Frontend App]
        API[API Gateway]
    end
    subgraph Edge["Edge Layer (Optional)"]
        Cache[Edge Cache Node]
    end

    Front --> API --> VM1 --> DB
    API --> Cache

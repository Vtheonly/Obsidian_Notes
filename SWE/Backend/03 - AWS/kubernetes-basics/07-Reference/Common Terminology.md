---
tags: [kubernetes, reference, glossary]
---

# Common Terminology

> [!summary] TL;DR
> Quick glossary of Kubernetes terms you'll meet daily. Bookmark this page.

## A–F

| Term                 | Short definition                                                          | See                 |
| -------------------- | ------------------------------------------------------------------------- | ------------------- |
| **API Server**       | Front door of the cluster; validates & persists all requests.             | [[Core Architecture]] |
| **Cluster**          | Control Plane + Nodes + shared state.                                     | [[Clusters]]        |
| **ConfigMap**        | Non-sensitive config key/value store.                                     | [[ConfigMaps and Secrets]] |
| **Container**        | A running instance of an image; the smallest unit Docker/containerd runs. | [[Pods]]            |
| **Controller**       | A control loop that drives actual state → desired state.                  | [[Core Architecture]] |
| **CNI**              | Container Network Interface plugin (Calico, Cilium, Flannel).             | [[Basic Networking]]|
| **CRD**              | Custom Resource Definition — extend the K8s API with your own objects.    | —                   |
| **Deployment**       | Manages rolling updates & rollback of Pods.                               | [[Deployments]]     |
| **etcd**             | Strongly-consistent KV store; source of truth for cluster state.          | [[Core Architecture]] |

## G–N

| Term                 | Short definition                                                          | See                 |
| -------------------- | ------------------------------------------------------------------------- | ------------------- |
| **HPA**              | Horizontal Pod Autoscaler.                                                | [[Basic Scaling]]   |
| **Image**            | A packaged, immutable container filesystem.                                | [[Pods]]            |
| **Ingress**          | HTTP-level routing & TLS termination for Services.                        | [[Basic Networking]]|
| **kube-proxy**       | Programs node network rules for Services.                                 | [[Nodes]]           |
| **kubelet**          | Node agent that ensures Pods are running.                                 | [[Nodes]]           |
| **kubectl**          | CLI for the Kubernetes API.                                               | [[Kubectl Commands]]|
| **Label**            | Key/value attached to objects for selection.                              | [[Pods]]            |
| **Namespace**        | Logical partition of a cluster.                                           | [[Namespaces]]      |
| **Node**             | A worker machine in the cluster.                                          | [[Nodes]]           |

## O–Z

| Term                 | Short definition                                                          | See                 |
| -------------------- | ------------------------------------------------------------------------- | ------------------- |
| **PersistentVolume** | Cluster storage resource.                                                 | [[Volumes]]         |
| **PersistentVolumeClaim** | User's request for PV storage.                                       | [[Volumes]]         |
| **Pod**              | Smallest deployable unit; one or more co-located containers.              | [[Pods]]            |
| **Probe**            | liveness / readiness / startup health check.                              | [[Pods]]            |
| **ReplicaSet**       | Maintains N identical Pods.                                               | [[ReplicaSets]]     |
| **Secret**           | Sensitive data store (base64-encoded).                                    | [[ConfigMaps and Secrets]] |
| **Selector**         | Label-based query used by Services, ReplicaSets, etc.                     | [[Services]]        |
| **Service**          | Stable network identity for a set of Pods.                                | [[Services]]        |
| **StatefulSet**      | Like Deployment but with stable identity & storage (for databases).       | —                   |
| **Taint / Toleration** | Repel pods from / admit pods to specific nodes.                         | [[Nodes]]           |
| **Volume**           | Storage attached to a Pod.                                                | [[Volumes]]         |

## Related Notes
- [[Best Practices for Beginners]] · [[Shared/readme]]

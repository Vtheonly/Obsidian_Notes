---
tags: [kubernetes, cli, kubectl]
---

# Kubectl Commands

> [!summary] TL;DR
> `kubectl` is the CLI you use to talk to the Kubernetes API. Master these commands and you can do 80% of daily work.

## Setup

```bash
# Install kubectl (Linux)
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Check
kubectl version --client
```

## The Five Verbs You'll Use Most

| Verb     | What it does                                  |
| -------- | --------------------------------------------- |
| `get`    | List resources                                |
| `describe` | Show detailed info                          |
| `apply`  | Create/update from a manifest                |
| `delete` | Remove a resource                             |
| `exec`   | Run a command inside a container              |

## Daily Cheat Sheet

```bash
# Cluster info
kubectl cluster-info
kubectl get nodes
kubectl get nodes -o wide

# Namespaces
kubectl get ns
kubectl config set-context --current --namespace=dev

# Pods
kubectl get pods                       # current namespace
kubectl get pods -A                    # all namespaces
kubectl get pods -o wide
kubectl describe pod <name>
kubectl logs <pod>
kubectl logs -f <pod>
kubectl exec -it <pod> -- sh

# Deployments
kubectl get deploy
kubectl describe deploy <name>
kubectl scale deploy/<name> --replicas=5
kubectl set image deploy/<name> <container>=<image>:<tag>
kubectl rollout status deploy/<name>
kubectl rollout undo deploy/<name>
kubectl rollout history deploy/<name>

# Services
kubectl get svc
kubectl describe svc <name>

# ConfigMaps & Secrets
kubectl get cm
kubectl get secret
kubectl describe cm <name>

# Apply / Delete
kubectl apply -f deploy.yaml
kubectl apply -f ./manifests/         # all yaml in dir
kubectl delete -f deploy.yaml
kubectl delete pod <name>

# Port-forward (local testing)
kubectl port-forward svc/hello-svc 8080:80
# then open http://localhost:8080

# Dry-run / explain (great for learning)
kubectl explain pod.spec.containers
kubectl apply -f deploy.yaml --dry-run=client -o yaml
```

## Output Formats

```bash
kubectl get pod <name> -o yaml         # full object
kubectl get pod <name> -o json
kubectl get pods -o wide               # with node/IP
kubectl get deploy -o custom-columns=NAME:.metadata.name,REPLICAS:.spec.replicas
```

## Useful Flags

| Flag            | Purpose                                                   |
| --------------- | --------------------------------------------------------- |
| `-n <ns>`       | Target namespace                                          |
| `-A`            | All namespaces                                            |
| `-o wide\|yaml\|json` | Output format                                       |
| `--watch` / `-w`| Stream updates                                            |
| `--selector` / `-l` | Filter by label                                       |
| `--dry-run=client` | Simulate without sending                              |

## Label & Selector Examples

```bash
kubectl get pods -l app=hello
kubectl get pods -l app=hello,tier=frontend
kubectl get pods --all-namespaces -l app=hello
```

## Aliases to Add to Your Shell

```bash
alias k=kubectl
alias kgp='kubectl get pods'
alias kgpw='kubectl get pods -o wide'
alias kgs='kubectl get svc'
alias kgd='kubectl get deploy'
alias kaf='kubectl apply -f'
alias kdf='kubectl delete -f'
source <(kubectl completion bash)   # tab completion
```

## Related Notes
- [[Deploy a Simple Application]] · [[Pods]] · [[Deployments]] · [[Services]]

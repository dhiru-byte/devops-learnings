# Kubernetes Networking – Interview Guide

This document covers **pod-to-pod communication, kube-proxy, iptables/IPVS, DNS resolution, and service types**.

---

## 1. How Does Pod-to-Pod Communication Work?

- Every Pod in Kubernetes gets a **unique IP**.
- Pods can communicate **directly** using this IP, across nodes if the CNI plugin supports it.
- Networking is **flat**: no NAT is required for Pod-to-Pod communication within a cluster network.
- CNI (Container Network Interface) plugins like **Calico, Flannel, Cilium** implement the actual network routing.

**Key points for interviews:**
- Every Pod can reach every other Pod (cluster-wide connectivity)
- Network plugins enforce network policies
- Cross-node Pod traffic is routed via the underlying network and overlay (VXLAN, BGP, or VxLAN/Geneve)

---

## 2. What is the Role of kube-proxy?

- kube-proxy runs on every node.
- Provides **Service → Pod communication**.
- Implements **virtual IPs** for services and routes traffic to the appropriate Pods.
- Maintains network rules via **iptables or IPVS**.

**Responsibilities:**
- Load balances traffic to backend Pods
- Handles Service discovery within a node
- Supports ClusterIP, NodePort, and LoadBalancer services

**One-liner:**  
> kube-proxy is the network bridge between Services and Pods, enabling traffic routing and load balancing.

---

## 3. iptables vs IPVS — Which One is Better and Why?

| Feature | iptables | IPVS |
|---------|----------|------|
| Scalability | Moderate | High (thousands of services) |
| Performance | Slower (linear lookup) | Faster (hash tables) |
| Load Balancing | Basic | Multiple algorithms (RR, LC, WRR, etc.) |
| Complexity | Simple | More complex setup |
| Resource Usage | Low | Low |

**Interview Summary:**  
> IPVS is generally preferred for production because of **higher scalability, performance, and advanced load balancing**, especially for large clusters.

---

## 4. How Does DNS Resolution Work Inside Kubernetes?

- CoreDNS (or kube-dns) provides cluster DNS.
- Pods can access services via **FQDN**: `<service>.<namespace>.svc.cluster.local`.
- Workflow:
  1. Pod queries DNS (usually CoreDNS)
  2. DNS resolves Service name to **ClusterIP**
  3. kube-proxy routes traffic from ClusterIP → backend Pod

**Key Points:**
- DNS is **automatically injected** into Pod via `/etc/resolv.conf`.
- Supports both **internal cluster services** and **external domains**.
- DNS is critical for service discovery in microservices.

---

## 5. Ingress vs LoadBalancer vs NodePort

| Service Type | Purpose | Use Case |
|-------------|---------|---------|
| **NodePort** | Opens a port on each Node | Dev/test or small clusters |
| **LoadBalancer** | External cloud LB for Service | Cloud environments (AWS ELB, GCP LB) |
| **Ingress** | Layer 7 routing / reverse proxy | HTTP(S) routing, path-based routing, TLS termination |

**Notes:**
- NodePort exposes service directly on Node IP.
- LoadBalancer depends on cloud provider integration.
- Ingress is more advanced, can route multiple services over the same IP, and manage TLS.

**One-liner:**  
> NodePort → basic access, LoadBalancer → cloud LB, Ingress → flexible HTTP routing.

---

## 🧠 Quick Interview Summary

- Pod-to-Pod: flat network, unique IP per Pod.
- kube-proxy: routes traffic from Service IPs to Pods.
- IPVS > iptables for production-scale clusters.
- CoreDNS handles service discovery.
- NodePort, LoadBalancer, Ingress: increasing sophistication and control over traffic.

---


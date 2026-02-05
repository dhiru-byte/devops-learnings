# Kubernetes Networking

This document covers **pod-to-pod communication, kube-proxy, iptables/IPVS, DNS resolution, and service types**.

---
<details>
<summary>  How Does Pod-to-Pod Communication Work? </summary><br><b>

- Every Pod in Kubernetes gets a **unique IP**.
- Pods can communicate **directly** using this IP, across nodes if the CNI plugin supports it.
- Networking is **flat**: no NAT is required for Pod-to-Pod communication within a cluster network.
- CNI (Container Network Interface) plugins like **Calico, Flannel, Cilium** implement the actual network routing.

**Key points for interviews:**
- Every Pod can reach every other Pod (cluster-wide connectivity)
- Network plugins enforce network policies
- Cross-node Pod traffic is routed via the underlying network and overlay (VXLAN, BGP, or VxLAN/Geneve)
</b></details>

<details>
<summary>  What is the Role of kube-proxy? </summary><br><b>

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
</b></details>

<details>
<summary>  iptables vs IPVS — Which One is Better and Why? </summary><br><b>

| Feature | iptables | IPVS |
|---------|----------|------|
| Scalability | Moderate | High (thousands of services) |
| Performance | Slower (linear lookup) | Faster (hash tables) |
| Load Balancing | Basic | Multiple algorithms (RR, LC, WRR, etc.) |
| Complexity | Simple | More complex setup |
| Resource Usage | Low | Low |

**Interview Summary:**  
> IPVS is generally preferred for production because of **higher scalability, performance, and advanced load balancing**, especially for large clusters.
</b></details>

<details>
<summary>  How Does DNS Resolution Work Inside Kubernetes? </summary><br><b>

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
</b></details>

<details>
<summary>  Difference between Ingress vs LoadBalancer vs NodePort. </summary><br><b>
  
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
## 🧠 Quick Interview Summary

- Pod-to-Pod: flat network, unique IP per Pod.
- kube-proxy: routes traffic from Service IPs to Pods.
- IPVS > iptables for production-scale clusters.
- CoreDNS handles service discovery.
- NodePort, LoadBalancer, Ingress: increasing sophistication and control over traffic.
</b></details>

<details>
<summary>  🚦 Kubernetes Traffic Routing: User-to-Pod Affinity Patterns </summary><br><b>

🏗️ Scenario 1: Network Level (ClientIP)

Managed by `kube-proxy` at the transport layer (Layer 4), this is the most basic form of "stickiness."

*   **Mechanism:** Uses the **Client's Source IP Address** as the hashing key.
*   **Best For:** Simple applications, non-HTTP protocols (TCP/UDP), or legacy services.
*   **Implementation:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: layer4-sticky-service
spec:
  selector:
    app: my-app
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800 # Time in seconds the affinity persists (default 10800)
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
```

* Limitation: Inaccurate if many users are behind a single NAT (e.g., a corporate office), as they will all be forced onto the same pod.

---
🚀 Scenario 2: Ingress Level (Cookie-Based)

Managed by the Ingress Controller at the application layer (Layer 7). This is the standard for modern web apps.

*   **Mechanism:** Injects a Session Cookie into the user's browser.
*   **Best For:** E-commerce sites, stateful UIs, and applications requiring high granularity.
*   **Implementation (NGINX Ingress):**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: layer7-sticky-ingress
  annotations:
    # Enable cookie-based affinity
    nginx.ingress.kubernetes.io/affinity: "cookie"
    # Name of the cookie to be injected
    nginx.ingress.kubernetes.io/session-cookie-name: "SERVERID"
    # Duration the cookie is valid
    nginx.ingress.kubernetes.io/session-cookie-expires: "172800"
    nginx.ingress.kubernetes.io/session-cookie-max-age: "172800"
spec:
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: my-service
            port:
              number: 80
```
Scenario 3: Service Mesh Level (Header-Based)

The most advanced method, providing programmatic control over traffic based on actual application data.

*   **Mechanism:** Inspects HTTP Headers (e.g., User-ID, JWT Token, or Version).
*   **Best For:** A/B Testing, Canary Rollouts, or VIP User routing (e.g., routing users with plan=premium to high-resource pods).
*   **Implementation (Istio VirtualService):**

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: premium-user-routing
spec:
  hosts:
  - my-service
  http:
  - match:
    - headers:
        # Matches a specific custom header
        x-user-type:
          exact: "premium"
    route:
    - destination:
        host: my-service
        subset: high-performance-pods
  - route:
    - destination:
        host: my-service
        subset: standard-pods
```

## Summary Comparison Matrix

| Feature | Service (ClientIP) | Ingress (Cookie) | Service Mesh (Header) |
| :--- | :--- | :--- | :--- |
| **OSI Layer** | Layer 4 (Transport) | Layer 7 (Application) | Layer 7 (Application) |
| **Routing Key** | Source IP | Browser Cookie | HTTP Header / JWT |
| **Granularity** | Low (IP-based) | High (Session-based) | Highest (User-based) |
| **Complexity** | Very Low | Moderate | High |

---

## 🔍 Key Takeaways for Interviews

*   **Layer 4 vs Layer 7:** Be ready to explain that `Service` level routing happens at the transport layer (TCP/UDP), whereas `Ingress` and `Service Mesh` operate at the application layer (HTTP/HTTPS), allowing them to "see" cookies and headers.
*   **The Proxy Problem:** Mention that **ClientIP** often fails in modern architectures because the [Load Balancer](https://kubernetes.io) or [Proxy](https://kubernetes.io) masks the real user IP unless `externalTrafficPolicy: Local` is used.
*   **Stateless vs Stateful:** While this table shows *how* to route to specific pods, always conclude by stating that **Stateless** design (using an external [Redis](https://aws.amazon.com) cache) is the preferred architectural pattern for scalability.
</b></details>

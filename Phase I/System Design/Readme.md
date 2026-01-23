
# System Design: Load Balancing, Scaling & Performance

## 1. Load Balancing (LB) & Traffic Management

Questions testing entry-point failure handling and traffic distribution.

### Global vs. Local Load Balancing
> How would you design a load-balancing strategy for an application with users in both Europe and North America? Where would you place DNS, and where would you place Anycast IPs?

### The "Sticky Session" Trade-off
> If our application requires session persistence (Sticky Sessions), how does that impact our ability to scale horizontally? What happens if a specific backend node becomes a 'hotspot'?

### L4 vs. L7 Deep Dive
> We are building a high-throughput video streaming service. Would you use a Layer 4 or Layer 7 load balancer at the edge? Why?

### Health Check Implementation
> Design a health-check mechanism for a load balancer that prevents the 'Zombieland' scenario (where an LB sends traffic to a service that is up but its database is down).

---

## 2. Vertical vs. Horizontal Scaling

Focus on the "When" and "How," rather than the "What."

### The Scaling Pivot Point
> We have a monolithic SQL database that is hitting 90% CPU. Walk me through the decision-making process: when do we stop upgrading the hardware (Vertical) and start sharding the data (Horizontal)?

### State Management
> How do you transition a stateful legacy application (storing files on local disk) to a horizontally scalable architecture? What are the risks of using a Distributed File System like NFS?

### Cost vs. Complexity
> Horizontal scaling is often more expensive due to networking overhead and dev-ops complexity. Can you argue for a case where staying 'Vertical' for as long as possible is the better business decision?

---

## 3. Latency vs. Throughput

Demonstrate optimization of one without destroying the other.

### The Batching Dilemma
> We need to process 1 million events per second. If we batch events to increase throughput, how will that affect our p99 latency? How do we find the 'sweet spot'?

### Identifying Bottlenecks
> A user reports that the 'Add to Cart' button takes 5 seconds. How do you trace the request to find if the bottleneck is network latency, disk I/O, or a locking contention in the database?

### Fan-out Architectures
> In a microservices environment, a single user request might trigger 20 downstream calls. How do you manage tail latency (the 'Slowest Leaf' problem) so it doesn't aggregate into a massive delay for the user?

---

## 4. Staff-Level Case Studies (Integration)

### Design a Global Rate Limiter
Focuses on latency vs scalability (10M requests/sec across 5 regions).

### Design a Flash Sale System
Focuses on horizontal scaling (100x spike) and load balancing (user queueing).

### Design a Metrics Monitoring System
Focuses on high throughput writes vs low latency reads for dashboards.

---

## Summary Checklist

- **Consistent Hashing**: Prevents re-sharding storms during horizontal scaling
- **CAP Theorem**: Horizontal database scaling forces Consistency/Availability trade-off
- **OSI Model**: Layers 3, 4, and 7; how LBs interact with them

# 🏗️ System Design: Key Architectural Archetypes

In high-level technical interviews, most "System Design" questions focus on specific architectural trade-offs. Below are three foundational archetypes categorized by their primary technical challenges.

---

### 1. Global Rate Limiter
**Primary Focus:** Latency vs. Scalability

A Global Rate Limiter must decide in milliseconds whether to allow or block a request, even when traffic is distributed across multiple geographic regions.

* **The Latency Challenge:** How fast can we check the limit? (e.g., using Redis with local replicas).
* **The Scalability Challenge:** Can the system handle **10M+ requests per second** across 5+ global regions without becoming a bottleneck?
* **Key Trade-off:** Strong Consistency (accurate counts) vs. Eventual Consistency (faster response times).



---

### 2. Flash Sale System (e.g., Black Friday)
**Primary Focus:** Horizontal Scaling vs. Load Management

Flash sale systems must survive extreme, sudden bursts of traffic where the load can spike **100x** within seconds.

* **Horizontal Scaling:** Rapidly spinning up instances to handle the spike.
* **Load Balancing & Queueing:** Using message queues (like Kafka or RabbitMQ) to buffer incoming requests, preventing the core database from collapsing under the pressure.
* **Key Pattern:** Decoupling the "Order Request" from "Order Processing" to ensure the UI remains responsive even if the backend is throttled.



---

### 3. Metrics Monitoring System (e.g., Datadog/Prometheus)
**Primary Focus:** Write Throughput vs. Read Latency

Monitoring systems deal with an "inverted" traffic pattern: constant, heavy writes with occasional, complex reads.

* **High Throughput Writes:** The system must ingest millions of data points per second from thousands of servers without dropping packets.
* **Low Latency Reads:** Dashboards and alerts must query this massive dataset and return results in seconds.
* **Storage Strategy:** Often involves **Time-Series Databases (TSDB)** and data downsampling (reducing resolution over time to save space).



---

### 📊 Summary Table

| Archetype | Main Bottleneck | Core Solution |
| :--- | :--- | :--- |
| **Rate Limiter** | Network Latency | Geo-distributed Caching (Redis) |
| **Flash Sale** | Database Write Contention | Async Processing (Queues) |
| **Metrics** | Storage Volume / Write Speed | Time-Series DB (LSM Trees) |
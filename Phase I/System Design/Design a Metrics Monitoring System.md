# System Design: Metrics Monitoring System (Datadog/Prometheus)

## 1. The Challenge
Design a system that collects, aggregates, and visualizes metrics from millions of servers and microservices.
* **Scale:** 100M active time series.
* **Throughput:** 10M writes per second.
* **Latency:** Dashboards must load in < 200ms.
* **Constraint:** Write-heavy workload (99% writes, 1% reads).

---

## 2. Requirements

### Functional Requirements
1.  **Ingestion:** Collect metrics (CPU, Memory, Request Count) from varied sources.
2.  **Storage:** Retain data with varying resolution (1 sec for 24h, 1 min for 30 days).
3.  **Querying:** Allow users to plot graphs and aggregate data (e.g., `avg(cpu) by region`).
4.  **Alerting:** Trigger notifications when thresholds are breached.

### Non-Functional Requirements
1.  **High Availability:** Losing metrics during an outage is acceptable; losing the ability to *see* the system is not.
2.  **Scalability:** Must handle linear growth in microservices/containers.
3.  **Low Latency:** Recent data must be queryable within seconds of occurrence.

---

## 3. High-Level Architecture

We can divide the system into four major pipelines: **Collection**, **Ingestion**, **Storage**, and **Query**.



### The Flow
1.  **Agents (Collection):** A lightweight daemon (DaemonSet in Kubernetes) runs on every host, scraping metrics.
2.  **Ingestion (Kafka):** Agents push metrics to a Load Balancer, which forwards them to **Kafka**. This acts as a shock absorber.
3.  **Stream Processor (Flink/Storm):** Consumes from Kafka to perform:
    * **Downsampling:** Aggregating raw data for long-term storage.
    * **Alerting:** Evaluating rules in real-time.
4.  **Time Series Database (TSDB):** The specialized storage engine optimized for time-stamped data (e.g., Cassandra, InfluxDB, or a custom Gorilla-like store).
5.  **Query Service:** APIs that fetch data for the frontend dashboards.

---

## 4. Deep Dive: Push vs. Pull Model (Staff Debate)

One of the first trade-offs a Staff Engineer must discuss.

| Model | Description | Pros | Cons |
| :--- | :--- | :--- | :--- |
| **Pull (Prometheus)** | Central server scrapes metrics from endpoints. | Easier to control load; easier to debug locally. | Hard to scale central server; requires service discovery; firewall issues. |
| **Push (Datadog)** | Agents send metrics to a central collector. | Works behind firewalls; ideal for short-lived jobs (serverless). | Easy to DDOS the backend; requires flow control. |

**Staff Decision:** For a global scale SaaS (like Datadog), we choose **Push** to support ephemeral containers and customer firewalls, but we implement **Aggregation at the Edge** to reduce traffic.

---

## 5. Deep Dive: Storage Layer (TSDB)

We cannot use a standard SQL DB. B-Trees are too slow for this write volume. We need an **LSM Tree** (Log-Structured Merge Tree) approach or a specialized TSDB.

### Data Model
* **Metric Name:** `http_requests_total`
* **Tags/Labels:** `{region="us-east", service="payment"}`
* **Timestamp:** `1674400000`
* **Value:** `42.5`

### Storage Optimization: Delta-of-Delta Encoding
(Reference: Facebook Gorilla Paper)
Instead of storing full 64-bit timestamps and values, we store the **difference**:
1.  Timestamp 1: `100` (Store full)
2.  Timestamp 2: `105` (Store `+5`)
3.  Timestamp 3: `110` (Store `0` - same delta)

This compresses data by **10x-12x**, allowing us to keep recent "hot" data entirely in RAM.

---

## 6. Data Aggregation & Downsampling (Rollups)

Storing 10M writes/second forever is impossibly expensive. We use **Rollups** (Downsampling).

### Retention Policy
* **Raw Data (1s resolution):** Keep for 24 hours. (Used for debugging).
* **Medium Data (1m resolution):** Keep for 30 days. (Used for daily trends).
* **Cold Data (1h resolution):** Keep for 1 year. (Used for monthly reports).

### Implementation
A **Stream Processor (Apache Flink)** reads the raw Kafka stream and produces new streams for the 1m and 1h buckets.
* *Write Amplification:* One incoming metric results in 3 writes (Raw, 1m, 1h), but the storage cost drops exponentially.



---

## 7. The Alerting System

Alerting must be separate from the standard query path to ensure reliability.

1.  **Evaluation Engine:** Reads rules from a configuration database.
2.  **In-Memory Window:** The engine subscribes to the Kafka stream and keeps a sliding window of data in memory (e.g., last 5 minutes).
3.  **Trigger:** If `avg(cpu) > 90%` for 5 mins, push an event to the **Notification Service** (PagerDuty/Slack).

**Staff Note:** Avoid "Query-based Alerting" (querying the DB every minute) for high-frequency alerts. It places massive read load on your TSDB. Use "Push-based Alerting" (evaluating the stream) instead.

---

## 8. Handling "Hot Partitions" (Staff Challenge)

**Scenario:** One customer (e.g., Amazon) sends 1000x more metrics than others. If we partition Kafka by `Customer_ID`, one partition becomes a bottleneck.

**Solution:**
1.  **Pre-Aggregation:** The Agent on the customer's side aggregates metrics before sending (e.g., send `p99` latency every 10s instead of every request).
2.  **Shuffle Sharding:** Instead of assigning a customer to 1 partition, assign them to a subset of virtual partitions to spread the load.

---

## 9. Summary of Trade-offs

| Decision | Trade-off |
| :--- | :--- |
| **Push Model** | Higher write load management complexity vs. Network accessibility. |
| **Downsampling** | Loss of precision in historical data vs. Massive cost savings. |
| **In-Memory Buffer** | Risk of data loss on crash (small gap) vs. High write throughput speed. |

# 📊 Observability Systems: The AP Design Archetype

For a Staff Engineer, the classification of Metrics and Logging systems is a classic example of **AP (Availability + Partition Tolerance)** design. In these systems, we prioritize **Ingestion (Availability)** over **Global Correctness (Consistency)**.

---

### 10. Metrics Systems (e.g., Prometheus, Datadog)
**Classification:** **AP**

* **The Logic:** If a network partition occurs between your application and the monitoring server, you want the application to keep running and the monitoring server to keep accepting data from other nodes. It is better to have a gap in your graph for 5 minutes (stale/missing data) than to have your entire application crash or hang because it couldn't "consistently" record a CPU metric.
* **PACELC Perspective (PA/EL):**
    * **P (Partition):** Favor **Availability** (keep the app running).
    * **E (Else/Normal):** Favor **Latency** (use UDP or asynchronous "fire and forget" writes so you don't slow down the main application).



---

### 11. Logging Systems (e.g., ELK Stack, Splunk)
**Classification:** **AP**

* **The Logic:** Logging is a "side-effect" of a transaction. If you are a bank, the **Transaction** itself is **CP**, but the **Log entry** saying "Transaction happened" is **AP**.
* **The Trade-off:** We use buffers (like Logstash or Fluentd) that hold logs in memory. If the connection to the central storage is lost, we might lose logs or they might arrive out of order (inconsistent). However, we would never stop a user from buying a product just because the "Log" system was having a network hiccup.
* **The Staff Nuance:** In specific legal or audit contexts (e.g., compliance logs), you might configure a system to be **CP**, where the app actually stops if it can't verify the log was written. But for 99% of observability, it is AP.



---

### 12. Comparison with Distributed Tracing (e.g., Jaeger)
**Classification:** **AP (Extremely AP)**

* **Logic:** Tracing is even more "Available" than Logging because we often use **Sampling**.
* **Design Choice:** We deliberately throw away 99% of the data to reduce overhead. Here, consistency is sacrificed by design to ensure the system's performance (**Latency**) and **Availability** are never impacted.

---

### 🔑 Staff Summary: Observability Trade-offs

| System Type | Consistency | Availability | Primary Trade-off |
| :--- | :--- | :--- | :--- |
| **Metrics** | Low (Stale data) | **High** | Latency over Accuracy |
| **Logging** | Medium (Buffers) | **High** | Throughput over Ordering |
| **Tracing** | Very Low (Sampling) | **Ultra-High** | Performance over Completeness |

> **Strategic Takeaway:** When designing for observability, always ask: *"Should the business logic wait for the telemetry to succeed?"* In AP systems, the answer is almost always **No**.
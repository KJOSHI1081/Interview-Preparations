# System Design: Flash Sale System (Black Friday/Ticketmaster)

## 1. The Challenge
A Flash Sale system is distinct from a standard e-commerce platform because it must handle **massive concurrency** on a **small subset of data**.
* **Traffic Pattern:** 10 million users arriving at exactly 12:00:00 PM.
* **Inventory:** Limited (e.g., 100 iPhones).
* **Constraint:** You strictly cannot oversell (Inventory must be accurate).

---

## 2. Requirements

### Functional Requirements
1.  **View Products:** Users can see item details before the sale starts.
2.  **Place Order:** Users can claim an item.
3.  **Payment:** Successful claims must be paid for within a time window (e.g., 5 mins).
4.  **Inventory Update:** Stock decreases in real-time.

### Non-Functional Requirements
1.  **High Availability:** The site must not crash under the spike.
2.  **Low Latency:** Users expect immediate feedback ("Did I get it?").
3.  **Consistency:** **Strict Consistency** for inventory counts (No overselling).
4.  **Fairness:** First come, first served. Bot protection is mandatory.

---

## 3. High-Level Architecture

We decouple the **"Buying Intent"** (high throughput) from the **"Order Processing"** (transactional integrity).



### The Flow
1.  **CDN:** Serves static assets (HTML/CSS/Images) to offload servers.
2.  **Virtual Waiting Room:** A gatekeeper layer to smooth out traffic spikes.
3.  **Inventory Service (Redis):** Handles the initial stock decrement (Atomic).
4.  **Message Queue (Kafka):** Buffers successful claims for processing.
5.  **Order Service (Workers):** Consumes messages, creates database records, and handles payments.

---

## 4. Deep Dive: Inventory Management (The Bottleneck)

**The Problem:** Standard SQL `UPDATE` locks rows. If 100,000 users try to lock the same row (Item ID #101), the database will deadlock or time out.

**The Solution:** In-Memory Atomic Counters (Redis).

### Implementation: Redis + Lua Scripting
We use Redis because it is single-threaded, making operations atomic by default. We use a **Lua Script** to ensure the "Check" and "Decrement" happen as one indivisible step.



```lua
-- Lua Script for atomic decrement
local key = KEYS[1]       -- The item ID (e.g., "item:101:stock")
local amount = ARGV[1]    -- Amount to buy (usually 1)

local current_stock = tonumber(redis.call('get', key))

if current_stock >= tonumber(amount) then
    redis.call('decrby', key, amount)
    return 1 -- Success
else
    return 0 -- Fail (Sold Out)
end
```
* **Pros:** Extremely fast (sub-millisecond), no DB locks.
* **Cons:** Redis persistence (RDB/AOF) must be tuned to prevent data loss if the cache node crashes.

---

## 5. Deep Dive: The "Virtual Waiting Room"

If traffic exceeds our system's maximum throughput (e.g., 1M requests/sec), we cannot simply reject users. We queue them.

1.  **The Gate:** When the user hits the "Buy" page, they are redirected to a queueing domain (e.g., `queue.mysite.com`).
2.  **The Token:** They receive a digitally signed token with their position.
3.  **The Leak Bucket:** We allow $N$ users per second to proceed to the actual checkout page based on our backend capacity.

**Staff-Level Note:** This protects downstream services from the "Thundering Herd" problem.

---

## 6. Asynchronous Order Processing

Once a user successfully decrements Redis, they have "reserved" the item. We do not write to the SQL database yet.

1.  **Publish:** The API server publishes an event `OrderCreated { user_id, item_id, timestamp }` to **Kafka**.
2.  **Consume:** A fleet of **Order Workers** reads from Kafka.
3.  **Persist:** The worker writes the order to the **Relational Database (PostgreSQL)** for ACID compliance.
4.  **Payment:** The worker triggers the Payment Gateway (Stripe/PayPal).



### Why this architecture?
* **Backpressure:** If the Database slows down, Kafka buffers the requests. The user has already received a "Success" message on the UI based on the Redis check.

---

## 7. Handling Failures & Edge Cases (The Staff Round)

### A. Payment Failure / Timeout
* **Scenario:** User reserves an iPhone but their credit card fails or they close the browser.
* **Solution:**
    * Redis keys act as a "Temporary Hold" with a **TTL (Time-To-Live)** of 10 minutes.
    * If the order isn't finalized in the DB within 10 minutes, a **Cleanup Worker** triggers a "Restock" event, incrementing the Redis counter back up.

### B. Overselling due to Redis Crash
* **Scenario:** Redis goes down after decrementing stock but before persisting to disk.
* **Solution:**
    * **Reconciliation:** We treat the SQL Database as the ultimate source of truth. Periodic scripts compare `Total_Inventory - Sold_Items_In_DB` vs `Redis_Counter`.
    * **Oversell Policy:** If we accidentally oversell by 5 items due to a crash, the business decision (Staff level thinking) is usually to cancel the last 5 orders and offer a gift card, rather than architecting an infinitely complex 100% consistent distributed transaction.

### C. Bot Prevention
* **Scenario:** Scripts buy all inventory in 1 millisecond.
* **Solution:**
    * **POW (Proof of Work):** Inject a JS challenge on the "Buy" button click.
    * **Limit per User:** Rate limit based on `User_ID`, `IP`, and `Device_Fingerprint`.
    * **CAPTCHA:** Trigger only if traffic patterns look anomalous.

---

## 8. Database Schema (Simplified)

We need a Relational DB for the final orders to ensure financial auditability.

**Table: Products**
| Column | Type | Notes |
| :--- | :--- | :--- |
| `id` | UUID | Primary Key |
| `name` | Varchar | |
| `total_stock` | Int | The hard limit |

**Table: Orders**
| Column | Type | Notes |
| :--- | :--- | :--- |
| `id` | UUID | Primary Key |
| `user_id` | UUID | Indexed for sharding |
| `item_id` | UUID | |
| `status` | Enum | `PENDING`, `PAID`, `FAILED` |
| `created_at` | Timestamp | |

* **Sharding:** We shard the **Orders** table by `user_id` so a single user always hits the same shard (good for "My Orders" history).

---

## 9. Summary of Trade-offs

| Decision | Trade-off |
| :--- | :--- |
| **Inventory in Redis** | We sacrifice absolute ACID consistency for extreme write throughput. We mitigate with reconciliation scripts. |
| **Async Processing** | We sacrifice immediate payment confirmation for system stability. Users get a "Processing" status first. |
| **Virtual Waiting Room** | We sacrifice User Experience (waiting) to prevent total system outage (Availability). |